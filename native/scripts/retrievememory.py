import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="chroma_db"  # can be changed for environments
))

collection = client.get_or_create_collection("memory")

def store_memory(message: str, user: str = "user", meta: dict = None):
    """Stores a message in memory."""
    metadata = meta or {}
    metadata.update({"speaker": user})
    
    collection.add(
        documents=[message],
        ids=[f"{user}_{collection.count()}"],
        metadata=[metadata]
    )

def retrieve_similar(query: str, top_k: int = 3):
    """Retrieves top_k similar memories."""
    results = collection.query(query_texts=[query], n_results=top_k)
    return results["documents"][0] if results["documents"] else []

def count_memory():
    return collection.count()

def reset_memory():
    client.delete_collection("memory")
