from typing import Callable

from functools import cached_property

from langchain_core.callbacks import CallbackManagerForRetrieverRun, AsyncCallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.embeddings import Embeddings

from weaviate.connect import ConnectionParams
from weaviate.classes.config import Property
from weaviate import WeaviateClient, WeaviateAsyncClient


class WeaviateRetriever(BaseRetriever):
    connection_params: ConnectionParams
    collection_name: str
    k: int = 5
    embeddings: Embeddings
    target_vector: str | list[str] | None = None
    format_properties_func: Callable[[list[Property]], str]

    @cached_property
    def client(self) -> WeaviateClient:
        return WeaviateClient(self.connection_params)

    @cached_property
    def async_client(self) -> WeaviateAsyncClient:
        return WeaviateAsyncClient(self.connection_params)

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> list[Document]:
        collection = self.client.collections.get(self.connection_name)
        embeded_query = self.embeddings.embed_query(query)
        response = collection.query.near_vector(
            near_vector=embeded_query,
            limit=self.k,
            target_vector=self.target_vector
        )
        documents: list[Document] = []
        for object in response.objects:
            page_content = self.format_properties_func(object.properties)
            documents.append(Document(page_content=page_content))
        return documents

    async def _aget_relevant_documents(
        self, query: str, *, run_manager: AsyncCallbackManagerForRetrieverRun
    ) -> list[Document]:
        collection = self.async_client.collections.get(self.connection_name)
        embeded_query = await self.embeddings.aembed_query(query)
        response = await collection.query.near_vector(
            near_vector=embeded_query,
            limit=self.k,
            target_vector=self.target_vector
        )
        documents: list[Document] = []
        for object in response.objects:
            page_content = self.format_properties_func(object.properties)
            documents.append(Document(page_content=page_content))
        return documents
