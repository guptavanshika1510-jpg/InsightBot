import requests
import json
from rag import load_pdf_text, index_pdf, get_relevant_context
from database import save_message
from intent import detect_intent   # 👈 NEW

OLLAMA_URL = "http://localhost:11434/api/generate"

# Track whether a PDF is indexed
pdf_indexed = False


# ==========================
# PDF UPDATE
# ==========================
def update_pdf(pdf_path):
    global pdf_indexed
    text = load_pdf_text(pdf_path)
    if text:
        index_pdf(text)
        pdf_indexed = True


# ==========================
# NORMAL (NON-STREAM) RESPONSE
# ==========================
def get_ai_response(user_message, use_pdf=False):
    save_message("user", user_message)

    # --------------------------
    # INTENT DETECTION
    # --------------------------
    intent = detect_intent(user_message, use_pdf)

    # --------------------------
    # SYSTEM / META INTENT
    # --------------------------
    if intent == "SYSTEM_MESSAGE":
        if pdf_indexed:
            return "✅ Document is already uploaded. You can ask questions about it."
        return "👋 Hi! Upload a PDF to start asking questions."

    # --------------------------
    # DOCUMENT SUMMARY (SAFE)
    # --------------------------
    if intent == "DOCUMENT_SUMMARY":
        if not pdf_indexed:
            return "⚠️ Please upload a document first."
        return (
            "📄 Full document summarization is not enabled yet.\n"
            "You can ask section-wise questions like:\n"
            "• What is Green Revolution?\n"
            "• Causes of Green Revolution\n"
            "• Advantages and disadvantages"
        )

    # --------------------------
    # DOCUMENT QUESTION ANSWERING
    # --------------------------
    if intent == "DOCUMENT_QA":
        if not pdf_indexed:
            return "⚠️ No document indexed. Please upload a PDF first."

        context = get_relevant_context(user_message)

        if not context.strip():
            return "The document does not contain this information."

        prompt = f"""
You are a document-grounded AI assistant.

STRICT RULES:
- Answer ONLY using the DOCUMENT CONTEXT.
- Do NOT use prior knowledge.
- Do NOT guess.
- If answer is missing, say:
  "The document does not contain this information."

DOCUMENT CONTEXT:
{context}

QUESTION:
{user_message}

FINAL ANSWER:
"""

    # --------------------------
    # GENERAL CHAT
    # --------------------------
    else:
        prompt = f"""
You are an AI assistant.

RULES:
- Be clear and concise.
- Do NOT greet.
- Do NOT mention yourself.

QUESTION:
{user_message}

ANSWER:
"""

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code != 200:
        return "⚠️ AI service error."

    ai_reply = response.json().get("response", "").strip()
    save_message("assistant", ai_reply)

    return ai_reply


# ==========================
# STREAMING RESPONSE (OPTIONAL)
# ==========================
def stream_ai_response(user_message, use_pdf=False):
    save_message("user", user_message)

    intent = detect_intent(user_message, use_pdf)

    if intent == "SYSTEM_MESSAGE":
        yield "✅ Document is already uploaded."
        return

    if intent == "DOCUMENT_SUMMARY":
        yield "📄 Full document summarization is not enabled yet."
        return

    context = ""

    if intent == "DOCUMENT_QA":
        if not pdf_indexed:
            yield "⚠️ No document indexed. Please upload a PDF first."
            return

        context = get_relevant_context(user_message)

        if not context.strip():
            yield "The document does not contain this information."
            return

        prompt = f"""
You are a document-grounded AI assistant.

STRICT RULES:
- Use ONLY document context.
- No prior knowledge.
- No guessing.

DOCUMENT CONTEXT:
{context}

QUESTION:
{user_message}

ANSWER:
"""
    else:
        prompt = f"""
You are an AI assistant.

RULES:
- Be concise.
- Do NOT greet.

QUESTION:
{user_message}

ANSWER:
"""

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": True
    }

    full_reply = ""

    with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                token = data.get("response", "")
                if token:
                    full_reply += token
                    yield token

    save_message("assistant", full_reply)
