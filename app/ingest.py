from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from app.config import DATA_DIR, VECTOR_DIR

model = SentenceTransformer("all-MiniLM-L6-v2")

import chromadb
from chromadb.config import Settings

chroma_client = chromadb.PersistentClient(path=VECTOR_DIR)

def load_documents(customer_type):
    folder = DATA_DIR / f"{customer_type}_docs"
    chunks = []
    for file in folder.iterdir():
        if file.is_file():
            with open(file, "r", encoding="utf-8") as f:
                chunks.extend([p.strip() for p in f.read().split("\n\n") if p.strip()])
    return chunks

def embed_and_store(customer_type):
    collection = chroma_client.get_or_create_collection(name=customer_type)
    chunks = load_documents(customer_type)
    embeddings = model.encode(chunks).tolist()

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"{customer_type}_{i}" for i in range(len(chunks))]
    )
    print(f"[{customer_type}] Stored {len(chunks)} chunks in ChromaDB")
