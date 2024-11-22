from llama_index.core import VectorStoreIndex, load_index_from_storage
from llama_index.core import StorageContext
from pinecone import Pinecone, ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
from src.global_settings import INDEX_STORAGE, PINECONE_INDEX_NAME

def build_indexes(nodes=None):
    pc = Pinecone()
    try:
        pinecone_index = pc.Index(PINECONE_INDEX_NAME)
        vector_store = PineconeVectorStore(
            pinecone_index=pinecone_index
        )
        vector_index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store
        )
        print("Remote indexes found.")
    except Exception as e:
        print(e)
        print("No indexes found. Creating new indexes...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            )
        )
        pinecone_index = pc.Index(PINECONE_INDEX_NAME)
        vector_store = PineconeVectorStore(
            pinecone_index=pinecone_index
        )
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )
        vector_index = VectorStoreIndex(
            nodes,
            storage_context=storage_context
        )
        print("New indexes created.")
    return vector_index