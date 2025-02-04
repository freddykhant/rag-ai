from langchain_ollama import ChatOllama
from langchain_nomic.embeddings import NomicEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# LLM setup
local_llm = "llama3.1:8b"
llm = ChatOllama(model=local_llm, temperature=0)

# Embeddings model setup
embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")

# Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=1024, chunk_overlap=200, length_function=len
)

# Retriever setup
# k = min(3, len(doc_splits)) # ensure k does not exceed available chunks
# retriever = vectorstore.as_retriever(
#             search_type="similarity_score_threshold",
#             search_kwargs={"k": k, "score_threshold": 0.1},
#         )