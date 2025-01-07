from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, END, StateGraph
import json
from state import SummaryState
from prompts import summary_prompt, router_instructions

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
  question = state["question"]

  documents = state["documents"]
  return {"documents": documents}

def generate(state):
  print("Generating summary...\n")
  question = state["question"]
  documents = state["documents"]
  loop_step = state.get("loop_step", 0)

  docs_txt = format_docs(documents)
  summary_prompt_formatted = summary_prompt.format(context=docs_txt, question=question)
  generation = llm.invoke([HumanMessage(content = summary_prompt_formatted)])
  return {"generation": generation.content, "loop_step": loop_step + 1}

def route_question(state):
  print("Routing question...\n")  
  route = llm_json_mode.invoke(
    [SystemMessage(content=router_instructions)]
    + HumanMessage(content=state["question"])
  )

  source = json.loads(route.content)["datasource"]
  if source == "generalinfo":
    print("Routing to general information...\n")
    return "generalinfo"
  elif source == "vectorstore":
    print("Routing to vectorstore...\n")
    return "vectorstore"
  
### Create Graph ###

builder = StateGraph(SummaryState)


# add nodes
builder.add_node("route_question", route_question)  
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)

# add edges
builder.set_conditional_entry_point(
  route_question,
  {
    "generalinfo": "generate",
    "vectorstore": "retrieve"
  }
)
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

graph = builder.compile()
