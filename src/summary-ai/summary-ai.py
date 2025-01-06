from langchain_ollama import ChatOllama
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_nomic.embeddings import NomicEmbeddings
from langchain_core.messages import HumanMessage
from prompts import summary_prompt 


# load LLM model
local_llm = "llama3.2:3b"
llm = ChatOllama(model=local_llm, temperature=0)