import os
from dotenv import load_dotenv
from src import RagDatasetGeneratorWithDelay
from src import ingest_pipeline
from src.prompts import QUESTION_GEN_QUERY_TEMPLATE
from llama_index.core.schema import Node
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
load_dotenv()

api_key = os.environ["GEMINI_API_KEY"]
Settings.llm = Gemini(model="models/gemini-1.5-flash-002", api_key=api_key)

if __name__=="__main__":
    # Use chunk 1024 for generating dataset
    nodes = ingest_pipeline.ingest_documents()
    print(len(nodes))
    num_questions_per_chunk = 1
    rag_dataset_generator = RagDatasetGeneratorWithDelay(
        nodes=nodes,
        num_questions_per_chunk=num_questions_per_chunk,
        question_gen_query=QUESTION_GEN_QUERY_TEMPLATE.format(num_questions_per_chunk=num_questions_per_chunk),
        delay_between_queries=5
        )
    rag_dataset_generator.generate_dataset_from_nodes().save_json("evaluate/data.json")