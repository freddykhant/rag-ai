from langchain_ollama import ChatOllama
from langchain_nomic.embeddings import NomicEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langgraph.graph import START, END, StateGraph
from langchain_chroma import Chroma
from typing_extensions import TypedDict, List
from dataclasses import dataclass, field

# LLM setup
local_llm = "llama3.1:8b"
llm = ChatOllama(model=local_llm, temperature=0)

# Embeddings model setup
embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")

# Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=1024, chunk_overlap=200, length_function=len
)

summary_prompt = PromptTemplate.from_template(
    """
    You are an expert in data analysis and summarization.

    Here is the dataset to analyze and summarize:
    {context}

    Here is the name of the file you need to summarize and analyze:
    {filename}

    Your task:
    1. Provide a concise summary of key trends, significant values, or patterns observed in the data.
    2. Highlight any notable details, such as outliers or frequent values.
    3. Make a brief inference or insight about the data, if possible, based on the provided information.

    Keep the summary to a maximum of three sentences and ensure the answer is clear, factual, and to the point.

    Answer:
    """
)

# Helper function to format documents
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# Define Graph Nodes
def retrieve(state):
    filename = state["filename"]
    # Load the vector store
    vectorstore = Chroma(persist_directory="db", embedding_function=embeddings)
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 20, "score_threshold": 0.1},
    )
    # Retrieve documents
    documents = retriever.get_relevant_documents(filename)
    return {"documents": documents}

def generate(state):
    filename = state["filename"]
    documents = state["documents"]
    docs_txt = format_docs(documents)

    summary_prompt_formatted = summary_prompt.format(context=docs_txt, filename=filename)
    generation = llm.invoke([HumanMessage(content=summary_prompt_formatted)])
    
    return {"generation": generation.content}

# State Definition
@dataclass(kw_only=True)
class SummaryState(TypedDict):
  filename : str = field(default=None)
  generation: str = field(default=None)
  documents: List[str] = field(default_factory=list)

# Build LangGraph Workflow
builder = StateGraph(SummaryState)
builder.add_node("retrieve", retrieve)
builder.add_node("generate", generate)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", END)

graph = builder.compile()

### TEST CODE FOR SUMMARY AI RAG PIPELINE, DO NOT DELETE ###

# input = SummaryState(filename="green_grocers_sales.csv")
# answer = graph.invoke(input)
# print(answer["generation"]) 