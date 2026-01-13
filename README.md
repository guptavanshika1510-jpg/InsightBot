# 🧠 InsightBot – AI Document Chatbot

InsightBot is a professional AI-powered chatbot that allows users to chat normally or ask questions from uploaded PDF documents using Retrieval-Augmented Generation (RAG).

## 🚀 Features
- Chat with AI (local LLM using Ollama)
- Upload PDF and ask document-based questions
- Toggle between normal chat and PDF mode
- Chat history stored in SQLite
- Dark mode UI
- Timestamped messages
- Responsive, modern UI

## 🛠 Tech Stack
- Python (Flask)
- SQLite
- Ollama (LLaMA 3)
- HTML, CSS, JavaScript

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/InsightBot.git
cd InsightBot
2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run Ollama
ollama run llama3
5️⃣ Start the app
python app.py
Open browser:
http://127.0.0.1:5000
Notes

PDFs are processed locally

No external API keys required

Works completely offline
Author

Vanshika Gupta

(Replace username later)

---

# ✅ STEP 4: INITIALIZE GIT (LOCAL)

In VS Code terminal (project root):

```bash
git init
git status
git add .
git commit -m "Initial commit: InsightBot AI Document Chatbot"

