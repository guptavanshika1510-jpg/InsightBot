import os
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_pdf_text(pdf_path):
    if not os.path.exists(pdf_path):
        return None

    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def get_relevant_context(query, pdf_text, top_k=3):
    if not pdf_text:
        return None

    chunks = pdf_text.split("\n\n")

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(chunks + [query])

    similarities = cosine_similarity(vectors[-1], vectors[:-1])
    top_indices = similarities[0].argsort()[-top_k:]

    return "\n".join([chunks[i] for i in top_indices])
