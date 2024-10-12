import asyncio
import re
import warnings
from typing import List
from llama_index.core import Document, SummaryIndex
from llama_index.core.async_utils import run_jobs
from llama_index.core.schema import MetadataMode, BaseNode
from llama_index.core.llama_dataset.generator import RagDatasetGenerator
from llama_index.core.llama_dataset import (
    CreatedBy,
    CreatedByType,
    LabelledRagDataExample,
    LabelledRagDataset,
)
from google.generativeai.types.generation_types import StopCandidateException

class RagDatasetGeneratorWithDelay(RagDatasetGenerator):
    def __init__(self, *args, delay_between_queries: int = 2, **kwargs):
        super().__init__(*args, **kwargs)
        self.delay_between_queries = delay_between_queries  # Add delay between queries
        
    async def _agenerate_dataset(
        self,
        nodes: List[BaseNode],
        labelled: bool = False,
    ) -> LabelledRagDataset:
        examples: List[LabelledRagDataExample] = []
        summary_indices: List[SummaryIndex] = []

        for num, node in enumerate(nodes):
            index = SummaryIndex.from_documents(
                [
                    Document(
                        text=node.get_content(metadata_mode=self._metadata_mode),
                        metadata=node.metadata,
                        excluded_llm_metadata_keys=node.excluded_llm_metadata_keys,
                        excluded_embed_metadata_keys=node.excluded_embed_metadata_keys,
                        relationships=node.relationships,
                    )
                ],
            )

            query_engine = index.as_query_engine(
                llm=self._llm,
                text_qa_template=self.text_question_template,
                use_async=True,
            )

            try:
                # Query and add delay
                response = await query_engine.aquery(self.question_gen_query)
            except StopCandidateException as e:
                # Handle exception when meeting the error StopCandidateException
                print(f"A safety error has occurred: {e}")
                continue  # Ignore and continue with next question

            summary_indices.append(index)

            # Add delay between queries
            await asyncio.sleep(self.delay_between_queries)

            result = str(response).strip().split("\n")
            cleaned_questions = [
                re.sub(r"^\d+[\).\s]", "", question).strip() for question in result
            ]
            cleaned_questions = [
                question for question in cleaned_questions if len(question) > 0
            ][: self.num_questions_per_chunk]

            num_questions_generated = len(cleaned_questions)
            if num_questions_generated < self.num_questions_per_chunk:
                warnings.warn(
                    f"Fewer questions generated ({num_questions_generated}) "
                    f"than requested ({self.num_questions_per_chunk})."
                )

            reference_context = node.get_content(metadata_mode=MetadataMode.NONE)
            model_name = self._llm.metadata.model_name
            created_by = CreatedBy(type=CreatedByType.AI, model_name=model_name)

            if labelled:
                qr_tasks = []
                for query in cleaned_questions:
                    qa_query_engine = index.as_query_engine(
                        llm=self._llm,
                        text_qa_template=self.text_qa_template,
                    )
                    qr_task = qa_query_engine.aquery(query)
                    qr_tasks.append(qr_task)

                for qr_task in qr_tasks:
                    try:
                        answer_response = await qr_task
                    except StopCandidateException as e:
                        print(f"A safety error has occurred when answering: {e}")
                        continue  # Ignore the question caused the error

                    example = LabelledRagDataExample(
                        query=query,
                        reference_answer=str(answer_response),
                        reference_contexts=[reference_context],
                        reference_answer_by=created_by,
                        query_by=created_by,
                    )
                    examples.append(example)

                    # Add delay between queries
                    await asyncio.sleep(self.delay_between_queries)
            else:
                for query in cleaned_questions:
                    example = LabelledRagDataExample(
                        query=query,
                        reference_answer="",
                        reference_contexts=[reference_context],
                        reference_answer_by=None,
                        query_by=created_by,
                    )
                    examples.append(example)
            
            print(f"Generated {num_questions_generated} question(s) for node {num + 1}/{len(nodes)}")

        return LabelledRagDataset(examples=examples)
