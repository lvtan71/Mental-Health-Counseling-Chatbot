from dotenv import load_dotenv
from llama_index.core.llama_dataset.generator import RagDatasetGenerator
from llama_index.core import Settings
from llama_index.core.prompts.base import PromptTemplate
from llama_index.llms.openai import OpenAI
from src import ingest_pipeline
from src.prompts import QUESTION_GEN_QUERY_TEMPLATE, TEXT_QA_TEMPLATE
from src.global_settings import DEFAULT_OPENAI_MODEL
load_dotenv()

Settings.llm = OpenAI(model=DEFAULT_OPENAI_MODEL)

if __name__=="__main__":
    # Use chunk 2048 for generating dataset
    nodes = ingest_pipeline.ingest_documents()
    print(len(nodes))
    num_questions_per_chunk = 3
    rag_dataset_generator = RagDatasetGenerator(
        nodes=nodes,
        num_questions_per_chunk=num_questions_per_chunk,
        text_qa_template=PromptTemplate(TEXT_QA_TEMPLATE),
        question_gen_query=QUESTION_GEN_QUERY_TEMPLATE.format(num_questions_per_chunk=num_questions_per_chunk),
    )
    rag_dataset_generator.generate_dataset_from_nodes().save_json("evaluate/data.json")