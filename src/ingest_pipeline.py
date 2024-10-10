import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.extractors import SummaryExtractor
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from src.global_settings import STORAGE_PATH, CACHE_FILE
from src.prompts import CUSTORM_SUMMARY_EXTRACT_TEMPLATE
load_dotenv()

api_key = os.environ["GEMINI_API_KEY"]
Settings.llm = Gemini(model="models/gemini-1.0-pro-001", api_key=api_key)
Settings.embed_model = GeminiEmbedding(model_name="models/text-embedding-004", api_key=api_key)

def ingest_documents():
    documents = SimpleDirectoryReader(
        STORAGE_PATH,
        filename_as_id=True
    ).load_data()

    for doc in documents:
        print(doc.id_)

    try:
        cached_hashes = IngestionCache.from_persist_path(
            CACHE_FILE 
        )
        print("Cache file found. Running using cache...")
    except:
        cached_hashes = ""
        print("No cache file found. Running without cache...")

    pipeline = IngestionPipeline(
        transformations=[
            TokenTextSplitter(
                chunk_size=512,
                chunk_overlap=20
            ),
            # SummaryExtractor(summaries=['self'], prompt_template=CUSTORM_SUMMARY_EXTRACT_TEMPLATE),
            GeminiEmbedding(model_name="models/text-embedding-004", api_key=api_key)
        ],
        cache=cached_hashes
    )

    nodes = pipeline.run(documents=documents)
    pipeline.cache.persist(CACHE_FILE)

    return nodes