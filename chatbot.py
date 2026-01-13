import requests
from rag import load_pdf_text, get_relevant_context
from database import save_message

OLLAMA_URL = "http://localhost:11434/api/generate"

# Global PDF text (can be updated at runtime)
pdf_text = None

# Conversation memory
conversation_history = []

def update_pdf(pdf_path):
    global pdf_text
    pdf_text = load_pdf_text(pdf_path)

def get_ai_response(user_message, use_pdf=False):
    # Save user message
    conversation_history.append(f"User: {user_message}")
    save_message("user", user_message)

    # Limit memory size
    history = "\n".join(conversation_history[-6:])

    context = None
    if use_pdf and pdf_text:
        context = get_relevant_context(user_message, pdf_text)

    # Build prompt
    if context:
        prompt = f"""
You are an AI assistant.
Rules:
- Do NOT greet the user.
- Do NOT comment on the conversation.
- Answer ONLY using the document context.
- Be concise and factual.

Conversation context:
{history}

Document context:
{context}

User question:
{user_message}

Answer:
"""
    else:
        prompt = f"""
You are an AI assistant.
Rules:
- Do NOT greet the user.
- Do NOT comment on the conversation.
- Answer directly and clearly.
- Be concise and informative.

Conversation context:
{history}

User question:
{user_message}

Answer:
"""

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        return "⚠️ Local AI error."

    data = response.json()
    ai_reply = data.get("response", "").strip()

    # Save AI reply
    conversation_history.append(f"Assistant: {ai_reply}")
    save_message("assistant", ai_reply)

    return ai_reply
