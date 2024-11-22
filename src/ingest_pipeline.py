import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.extractors import SummaryExtractor
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from src.global_settings import (STORAGE_PATH,
                                 CACHE_FILE,
                                 DEFAULT_HUGGINGFACE_EMBEDDING,
                                 CACHE_MODEL_DIR,
                                 DEFAULT_GEMINI_MODEL,
                                 DEFAULT_GEMINI_EMBEDDING
                                 )
import nest_asyncio

nest_asyncio.apply()
load_dotenv()

Settings.llm = Gemini(model=DEFAULT_GEMINI_MODEL)
Settings.embed_model = GeminiEmbedding(model_name=DEFAULT_GEMINI_EMBEDDING)

def ingest_documents():

    # parser = LlamaParse(
    #     result_type="markdown",
    #     verbose=True,
    #     language="vi",
    # )

    # file_extractor = {".pdf": parser}

    # documents = SimpleDirectoryReader(
    #     STORAGE_PATH,
    #     filename_as_id=True,
    #     file_extractor=file_extractor,
    # ).load_data()

    documents = SimpleDirectoryReader(
        os.path.join(STORAGE_PATH, "temp"),
        filename_as_id=True,
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
            Settings.embed_model,
        ],
        cache=cached_hashes
    )

    nodes = pipeline.run(documents=documents)
    pipeline.cache.persist(CACHE_FILE)

    return nodes