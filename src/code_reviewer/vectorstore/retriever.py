from typing import Any

import logging

from weaviate import WeaviateAsyncClient
from weaviate.collections import CollectionAsync

from ..core.base import VectorStoreRetriever

logger = logging.getLogger(__name__)


class WeaviateRetriever(VectorStoreRetriever):
    def __init__(self, client: WeaviateAsyncClient, schema: dict[str, Any]) -> None:
        self.client = client
        self.schema = schema

    async def _get_or_create_collection(self) -> ...:
        is_exists = await self.client.collections.exists(self.schema["class"])
        if not is_exists:
            collection = await self.client.collections.create_from_config(self.schema)
        else:
            ...

    async def similarity_search(self, query: str) -> list[dict[str, str]]:
        ...
