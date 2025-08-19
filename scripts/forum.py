from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.code_reviewer.settings import BASE_DIR, settings

FILE_PATH = BASE_DIR / "assets" / "docs" / "forum" / "qa.txt"

with open(FILE_PATH, encoding="utf-8") as file:
    text = file.read()

embeddings = HuggingFaceEmbeddings(
    model_name="deepvk/USER-bge-m3",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False},
)

vectorstore = PineconeVectorStore(
    embedding=embeddings, pinecone_api_key=settings.pinecone.api_key, index_name="1c-forum"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=20,
    length_function=len
)

chunks = splitter.split_documents([Document(page_content=text)])

vectorstore.add_documents(chunks)
