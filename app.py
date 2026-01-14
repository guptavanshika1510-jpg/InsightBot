import os
from flask import Flask, render_template, request, jsonify, Response
from werkzeug.utils import secure_filename

from chatbot import stream_ai_response, update_pdf
from database import init_db, get_all_messages

app = Flask(__name__)
init_db()

UPLOAD_FOLDER = "data/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# HOME
# =========================
@app.route("/")
def index():
    return render_template("index.html")

# =========================
# STREAM CHAT (LIVE TOKENS)
# =========================
@app.route("/chat_stream", methods=["POST"])
def chat_stream():
    data = request.json
    user_message = data.get("message", "")
    use_pdf = data.get("use_pdf", False)

    def generate():
        for chunk in stream_ai_response(user_message, use_pdf):
            yield chunk

    return Response(generate(), mimetype="text/plain")

# =========================
# UPLOAD PDF
# =========================
@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    file = request.files.get("pdf")
    if not file:
        return jsonify({"message": "No file uploaded."})

    path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
    file.save(path)
    update_pdf(path)

    return jsonify({"message": "PDF indexed successfully."})

# =========================
# CHAT HISTORY
# =========================
@app.route("/history")
def history():
    return jsonify(get_all_messages())

if __name__ == "__main__":
    app.run(debug=True)
