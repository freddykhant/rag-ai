from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from rag import llm, embeddings, text_splitter, SummaryState, graph

# Initialise Flask
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure necessary directories exist
folder_path = "db"
if not os.path.exists("files"):
    os.makedirs("files")

## API Routes ##

# Health Check Route
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# Upload Route
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    file_name = file.filename
    save_file = os.path.join("files", file_name)
    file.save(save_file) # saves file at the specified path
    logger.info(f"File saved at {save_file}")

    try:
        loader = CSVLoader(save_file)
        docs = loader.load()
        logger.info(f"Documents loaded: {len(docs)}")

        chunks = text_splitter.split_documents(docs)
        logger.info(f"Chunks created: {len(chunks)}")   

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=folder_path,
        )

        vectorstore.persist()

        return jsonify({"status": "success", "filename": file_name, "doc_len": len(docs)}), 200
    
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return jsonify({"error": "Failed to upload file"}), 500
    
# Summary Route
@app.route("/summary", methods=["POST"])
def summary():
    data = request.json
    filename = data.get("filename")

    if not filename:
        return jsonify({"error": "Filename is required"}), 400

    logger.info(f"Filename received: {filename}")

    try:
        input_state = SummaryState(filename=filename)
        result = graph.invoke(input_state)
        summary_text = result.get("generation", "No summary generated.")

        return jsonify({"summary": summary_text}), 200

    except Exception as e:
        logger.error(f"Error in summarization: {e}")
        return jsonify({"error": "Failed to generate summary"}), 500

# Run Flask Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)