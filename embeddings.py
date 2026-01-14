import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Global index and data
index = None
documents = []

def create_embeddings(chunks):
    global index, documents
    documents = chunks

    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

def search_embeddings(query, top_k=3):
    if index is None:
        return []

    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    return [documents[i] for i in indices[0]]
