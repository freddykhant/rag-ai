from langchain_core.messages import HumanMessage
from langgraph.graph import START, END, StateGraph
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from state import SummaryState
from prompts import summary_prompt
from setup import retriever, text_splitter
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

# Initialise Flask
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ensure necessary directories exist
folder_path = "db"
if not os.path.exists("files"):
    os.makedirs("files")

# Helper function to format documents
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# Define Graph Nodes
def retrieve(state):
    filename = state["filename"]
    documents = retriever.invoke(filename)
    return {"documents": documents}

def generate(state):
    filename = state["filename"]
    documents = state["documents"]
    docs_txt = format_docs(documents)

    summary_prompt_formatted = summary_prompt.format(context=docs_txt, filename=filename)
    generation = llm.invoke([HumanMessage(content=summary_prompt_formatted)])
    
    return {"generation": generation.content}

# Build LangGraph Workflow
builder = StateGraph(SummaryState)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

graph = builder.compile()

## API Routes 

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

# Run Flask Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


### TEST CODE FOR SUMMARY AI RAG PIPELINE, DO NOT DELETE ###

# input = SummaryState(filename="green_grocers_sales.csv")
# answer = graph.invoke(input)
# print(answer["generation"]) 