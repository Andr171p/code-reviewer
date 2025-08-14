from langchain_core.documents import Document
from langchain_community.document_loaders import GithubFileLoader
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.code_reviewer.settings import settings

SEPARATORS = [
    "\n\n",                 # Двойной перенос (разделяет крупные блоки)
    "\n",                   # Одиночный перенос
    "КонецПроцедуры",       # Конец процедуры
    "КонецФункции",         # Конец функции
    "Процедура ",           # Начало процедуры (с пробелом, чтобы не ловить "Процедура" в тексте)
    "Функция ",             # Начало функции (аналогично)
    ";",                    # Конец строки
    " ",                    # Пробел (последний приоритет)
]

REPO = "dns-technologies/SDMS"
OUTPUT_DIR = REPO.split("/")[-1]


def file_filter(filename: str) -> bool:
    if filename.split(".")[-1] in ("os", "md", "bsl"):
        return True
    return False


loader = GithubFileLoader(
    repo=REPO,
    branch="main",
    access_token=settings.github.access_token,
    github_api_url="https://api.github.com",
    file_filter=file_filter,
)

documents = loader.load()

print(len(documents))

chunks: list[Document] = []
for document in documents:
    if document.metadata.get("path").split(".")[-1] in ("bsl", "os"):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=20,
            length_function=len,
            separators=SEPARATORS,
        )
        docs = splitter.split_documents([document])
        chunks.extend(docs)
    if document.metadata.get("path").split(".")[-1] == "md":
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=20,
            length_function=len
        )
        docs = splitter.split_documents([document])
        chunks.extend(docs)

print(len(chunks))

embeddings = HuggingFaceEmbeddings(
    model_name=settings.embeddings.model_name,
    model_kwargs=settings.embeddings.model_kwargs,
    encode_kwargs=settings.embeddings.encode_kwargs,
)

vectorstore = PineconeVectorStore(
    pinecone_api_key=settings.pinecone.api_key,
    embedding=embeddings,
    index_name="1c-code"
)


print("Загрузка репозитория")
vectorstore.add_documents(chunks)
