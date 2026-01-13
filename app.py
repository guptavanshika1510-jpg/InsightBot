import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from chatbot import get_ai_response, update_pdf
from database import init_db, get_all_messages

app = Flask(__name__)

init_db()

UPLOAD_FOLDER = "data/uploads"
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    reply = get_ai_response(
        data.get("message"),
        data.get("use_pdf", False)
    )
    return jsonify({"reply": reply})

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    file = request.files.get("pdf")
    if not file or file.filename == "":
        return jsonify({"message": "No file selected."})

    if allowed_file(file.filename):
        path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
        file.save(path)
        update_pdf(path)
        return jsonify({"message": "PDF uploaded successfully."})

    return jsonify({"message": "Invalid file type."})

@app.route("/history", methods=["GET"])
def history():
    return jsonify(get_all_messages())

if __name__ == "__main__":
    app.run(debug=True)
