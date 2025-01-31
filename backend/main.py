from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import START, END, StateGraph
from state import SummaryState
from prompts import summary_prompt, answer_prompt
from vectordb import retriever
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

# Initialise Flask
app = Flask(__name__)
CORS(app)

# LLM setup
local_llm = "llama3.2:3b"
llm = ChatOllama(model=local_llm, temperature=0)

# Helper function to format documents
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# Define Graph Nodes
def retrieve(state):
    topic = state["topic"]
    documents = retriever.invoke(topic)
    return {"documents": documents}

def generate(state):
    topic = state["topic"]
    documents = state["documents"]
    docs_txt = format_docs(documents)

    summary_prompt_formatted = summary_prompt.format(context=docs_txt, topic=topic)
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

# API Route
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "Missing topic"}), 400

    input_state = SummaryState(topic=topic)
    result = graph.invoke(input_state)

    return jsonify({"summary": result["generation"]})

# Run Flask Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)