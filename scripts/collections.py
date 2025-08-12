from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from src.code_reviewer.settings import BASE_DIR, settings

DIRECTORY = BASE_DIR / "assets" / "docs" / "its" / "dev_rules"

embeddings = HuggingFaceEmbeddings(
    model_name="deepvk/USER-bge-m3",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False},
)

vectorstore = PineconeVectorStore(
    embedding=embeddings, pinecone_api_key=settings.pinecone.api_key, index_name="1c-best-practice"
)

"""splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=20,
    length_function=len
)

files = Path(DIRECTORY).glob("**/*.txt")

for file in files:
    content = file.read_text(encoding="utf-8")
    print(f"Count of chars in {file.name}")
    print(len(content))
    documents = splitter.split_documents([
        Document(
            page_content=content,
            metadata={"filename": file.name, "source": "https://1c.its.ru"},
        )
    ])
    print(f"Split documents")
    print(len(documents))
    vectorstore.add_documents(documents)
    print("Successfully add documents")"""


query = "Какая правильная структура модуля"

docs = vectorstore.similarity_search(query=query, k=7)

for doc in docs:
    print(75 * "=")
    print(doc)
