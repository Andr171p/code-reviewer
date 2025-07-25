import logging

import weaviate

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_gigachat import GigaChat

from src.code_reviewer.splitters.separators import BSL_SEPARATORS
from src.code_reviewer.loaders import BSLContextEnrichmentDirectoryLoader

logging.basicConfig(level=logging.INFO)

embeddings = HuggingFaceEmbedding(
    model_name="deepvk/USER-bge-m3", device="cpu"
)

# DIR_PATH = r"C:\Users\andre\CodeReviewer\assets\1С_Бухгалтерия"

DIR_PATH = r"C:\Users\andre\Downloads\1С_Бухгалтерия"

llm = GigaChat(
    credentials="",
    scope="",
    model="",
    verify_ssl_certs=False,
    profanity_check=False
)

loader = BSLContextEnrichmentDirectoryLoader(
    dir_path=DIR_PATH,
    llm=llm
)

documents = loader.load()

print(len(documents))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=20,
    length_function=len,
    separators=BSL_SEPARATORS
)

chunks = splitter.split_documents(documents)

print(len(chunks))

client = weaviate.connect_to_custom(
    http_host="10.1.50.85",
    http_port=8090,
    http_secure=False,
    grpc_host="10.1.50.85",
    grpc_port=50051,
    grpc_secure=False
)

client.is_ready()

modules = client.collections.get("Modules")

objects = [
    {
        "project": chunk.metadata["project"],
        "filename": chunk.metadata["filename"],
        "file_path": chunk.metadata["file_path"],
        "content": chunk.page_content,
        "type": chunk.metadata.get("type"),
        "purpose": chunk.metadata.get("purpose"),
        "detail": chunk.metadata.get("detail")
    }
    for chunk in chunks
]

with modules.batch.fixed_size() as batch:
    for object in objects:
        batch.add_object(
            properties=object,
            vector={
                "project": embeddings.get_text_embedding(object["project"]),
                "filename": embeddings.get_text_embedding(object["filename"]),
                "file_path": embeddings.get_text_embedding(object["file_path"]),
                "content": embeddings.get_text_embedding(object["content"]),
                "type": embeddings.get_text_embedding(object["type"]),
                "purpose": embeddings.get_text_embedding(object["purpose"]),
                "detail": embeddings.get_text_embedding(object["detail"])
            }
        )

client.close()
