import os
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# ==========================
# MODEL & STORAGE
# ==========================
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

vector_index = None
chunks_store = []


# ==========================
# PDF LOADER
# ==========================
def load_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


# ==========================
# TEXT CHUNKING
# ==========================
def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# ==========================
# INDEX PDF (EMBEDDINGS)
# ==========================
def index_pdf(text):
    global vector_index, chunks_store

    chunks_store = chunk_text(text)

    embeddings = EMBEDDING_MODEL.encode(chunks_store)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]
    vector_index = faiss.IndexFlatL2(dimension)
    vector_index.add(embeddings)


# ==========================
# RETRIEVE CONTEXT
# ==========================
def get_relevant_context(query, top_k=4):
    if vector_index is None:
        return ""

    query_embedding = EMBEDDING_MODEL.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = vector_index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(chunks_store):
            results.append(chunks_store[idx])

    return "\n\n".join(results)
