from __future__ import annotations

import logging

from weaviate import WeaviateAsyncClient, WeaviateClient
from weaviate.classes.config import Property

from langchain_core.embeddings import Embeddings
from langchain_core.tools import BaseTool
from pydantic import model_validator

logger = logging.getLogger(__name__)


class BaseWeaviateSearchTool(BaseTool):
    client: WeaviateClient | None = None
    async_client: WeaviateAsyncClient | None = None
    embeddings: Embeddings | None = None
    collection_name: str | None = None

    @classmethod
    def from_client(
            cls,
            client: WeaviateClient | None = None,
            async_client: WeaviateAsyncClient | None = None,
            embeddings: Embeddings | None = None
    ) -> BaseWeaviateSearchTool:
        return cls(client=client, async_client=async_client)

    @model_validator(mode="before")
    def validate_client_provided(self) -> BaseWeaviateSearchTool:
        if self.client is None and self.async_client is None:
            raise ValueError("Either clients instances must be provided!")
        return self

    def _run(self, query: str, limit: int) -> str:
        logger.info("---SEARCH %s---", self.collection_name.upper())
        if self.collection_name is None:
            raise ValueError("Collection name must be defined!")
        collection = self.client.collections.get(self.collection_name)
        embeded_query = self.embeddings.embed_query(query)
        response = collection.query.near_vector(embeded_query, limit=limit)
        formated_properties: list[str] = []
        for object in response.objects:
            formated_properties.append(
                self._format_properties(object.properties)
            )
        return "\n\n".join(formated_properties)

    async def _arun(self, query: str, limit: int) -> str:
        logger.info("---SEARCH %s---", self.collection_name.upper())
        if self.collection_name is None:
            raise ValueError("Collection name must be defined!")
        collection = self.async_client.collections.get(self.collection_name)
        embeded_query = await self.embeddings.aembed_query(query)
        response = await collection.query.near_vector(embeded_query, limit=limit)
        formated_properties: list[str] = []
        for object in response.objects:
            formated_properties.append(
                self._format_properties(object.properties)
            )
        return "\n\n".join(formated_properties)

    def _format_properties(self, properties: list[Property]) -> str:
        raise NotImplementedError
