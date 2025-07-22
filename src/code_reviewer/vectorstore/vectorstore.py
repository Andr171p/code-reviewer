from __future__ import annotations

from typing import Any

import logging
from functools import cached_property

from weaviate import WeaviateClient, WeaviateAsyncClient

from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

logger = logging.getLogger(__name__)


class WeaviateVectorStore(VectorStore):
    def __init__(
            self,
            connection_params: dict[str, str | int],
            schema: dict[str, Any] | None = None,
            embeddings: Embeddings | None = None,
    ) -> None:
        self._connection_params = connection_params
        self._schema = schema
        self._embeddings = embeddings

    @cached_property
    def async_client(self) -> WeaviateAsyncClient:
        return WeaviateAsyncClient(**self._connection_params)

    @cached_property
    def client(self) -> WeaviateClient:
        return WeaviateClient(**self._connection_params)
