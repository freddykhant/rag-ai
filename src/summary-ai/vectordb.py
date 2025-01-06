from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_nomic.embeddings import NomicEmbeddings  

# vector store
files = [
  "data/coffee_heaven_sales.csv",
  "data/tech_emporium_sales.csv",
  "data/green_grocers_sales.csv"
]

# load documents
docs = []
for file in files:
  loader = CSVLoader(file)
  docs += loader.load()

# split documents
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
  chunk_size=1000, chunk_overlap=200
)

doc_splits = text_splitter.split_documents(docs)

# add to vector database
vectorstore = SKLearnVectorStore.from_documents(
  documents=doc_splits,
  embedding=NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")
)

# create retriever
k = min(3, len(doc_splits)) # ensure k does not exceed available chunks
retriever = vectorstore.as_retriever(k=k)