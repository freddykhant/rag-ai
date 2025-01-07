from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import START, END, StateGraph
import json
from state import SummaryState
from prompts import summary_prompt
from vectordb import retriever

# LLM
local_llm = "llama3.2:3b"
llm = ChatOllama(model=local_llm, temperature=0)
llm_json_mode = ChatOllama(model=local_llm, temperature=0, mode="json") 

# helper method to format documents
def format_docs(docs):
  return "\n\n".join([doc.page_content for doc in docs])

# node methods

def retrieve(state):
  print("Retrieving documents...\n")
  topic = state["topic"]

  documents = retriever.invoke(topic)
  return {"documents": documents}

def generate(state):
  print("Generating summary...\n")
  topic = state["topic"]
  documents = state["documents"]
  loop_step = state.get("loop_step", 0)

  docs_txt = format_docs(documents)
  summary_prompt_formatted = summary_prompt.format(context=docs_txt, topic=topic)
  generation = llm.invoke([HumanMessage(content = summary_prompt_formatted)])
  return {"generation": generation.content, "loop_step": loop_step + 1}
  
### Create Graph ###

builder = StateGraph(SummaryState)

# add nodes
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)

# add edges
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

graph = builder.compile()

# test run

input = SummaryState(
  topic = "Sales"
)
summary = graph.invoke(input)

print(summary["generation"])