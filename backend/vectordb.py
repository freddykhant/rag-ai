from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_nomic.embeddings import NomicEmbeddings  

# embeddings model setup
embeddings = NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")

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
text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=1024, chunk_overlap=200, length_function=len
)

doc_splits = text_splitter.split_documents(docs)

# add to vector database
vectorstore = Chroma.from_documents(
  documents=doc_splits,
  embedding=embeddings
)

# create retriever
k = min(3, len(doc_splits)) # ensure k does not exceed available chunks
retriever = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": k, "score_threshold": 0.1},
        )