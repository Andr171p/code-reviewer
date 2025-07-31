import os
from dotenv import load_dotenv

import weaviate
from llama_index.readers.file import PyMuPDFReader
from llama_index.core.node_parser import LangchainNodeParser
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

PDF_PATH = (
    r"C:\Users\andre\CodeReviewer\assets\docs\Руководство-пользователя-83.004.04.pdf"
)

embeddings = HuggingFaceEmbedding(
    model_name="deepvk/USER-bge-m3", device="cpu"
)

reader = PyMuPDFReader()

documents = reader.load(PDF_PATH)

for document in documents:
    document.metadata["filename"] = document.metadata["file_path"].split("\\")[-1]

node_parser = LangchainNodeParser(RecursiveCharacterTextSplitter(
    chunk_size=1024,
    chunk_overlap=20,
    length_function=len
))

nodes = node_parser.get_nodes_from_documents(documents)

client = weaviate.connect_to_custom(
    http_host=os.getenv("WEAVIATE_HTTP_HOST"),
    http_port=os.getenv("WEAVIATE_HTTP_PORT"),
    http_secure=False,
    grpc_host=os.getenv("WEAVIATE_GRPC_HOST"),
    grpc_port=os.getenv("WEAVIATE_GRPC_PORT"),
    grpc_secure=False
)

client.is_ready()

nodes = nodes[:50]

objects = [
    {
        "source": node.metadata.get("filename"),
        "content": node.text,
        "page": int(node.metadata.get("source")),
        "total_pages": int(node.metadata.get("total_pages"))
    }
    for node in nodes
]

docs = client.collections.get("Docs")

with docs.batch.fixed_size(batch_size=len(objects)) as batch:
    for object in objects:
        embedding = embeddings.get_text_embedding(object["content"])
        batch.add_object(
            properties=object,
            vector={"content": embedding}
        )


query = "Какие лучшие практики создания метаданных?"

vector = embeddings.get_text_embedding(query)

documentations = client.collections.get("Docs")

response = documentations.query.near_vector(vector)

print(response)

for object in response.objects:
    print(object.properties["content"])

client.close()
