from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
from app.config import VECTOR_DIR

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Use PersistentClient (new API)
chroma_client = chromadb.PersistentClient(path=VECTOR_DIR)

# Retrieve chunks
def retrieve_chunks(customer_type, query):
    try:
        collection = chroma_client.get_collection(name=customer_type)
    except:
        return {"error": f"No collection found for '{customer_type}'"}

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=10
    )

    return {
        "query": query,
        "results": results["documents"][0] if results["documents"] else []
    }
