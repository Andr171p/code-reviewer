from weaviate import WeaviateAsyncClient
from sentence_transformers import SentenceTransformer

from .base import BaseVectorStore
from .schemas import Document


class WeaviateVectorStore(BaseVectorStore):
    def __init__(
            self,
            client: WeaviateAsyncClient,
            collection_name: str,
            vectorizer: SentenceTransformer,
    ) -> None:
        self.client = client
        self.collection_name = collection_name
        self.vectorizer = vectorizer

    async def similarity_search(
            self, query: str, distance_threshold: float, limit: int, **kwargs
    ) -> list[Document]:
        collection = self.client.collections.get(self.collection_name)
        embedding = self.vectorizer.encode(query)
        response = await collection.query.near_vector(
            near_vector=embedding,
            limit=limit,
            target_vector="content",
        )
        documents: list[Document] = []
        for object in response.objects:
            document = Document.model_validate(
                object.properties, context={"id": object.id, "metadata": object.metadata}
            )
            documents.append(document)
        return documents

    async def add(self, documents: list[Document], **kwargs) -> None:
        collection = self.client.collections.get(self.collection_name)
        objects = [
            {
                "uuid": document.id,
                "properties": document.model_dump(exclude={"id", "metadata"}),
                "vector": {"content": self.vectorizer.encode(document.content).tolist()},
                "metadata": document.metadata,
            }
            for document in documents
        ]
        await collection.data.insert_many(objects)
