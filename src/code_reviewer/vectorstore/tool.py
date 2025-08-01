from __future__ import annotations

from typing import Callable

import logging

from langchain_core.tools import BaseTool
from langchain_core.embeddings import Embeddings

from weaviate.connect import ConnectionParams
from weaviate.classes.config import Property

from .retriever import WeaviateRetriever
from src.code_reviewer.agent.utils import format_documents

logger = logging.getLogger(__name__)


class BaseWeaviateRetrieverTool(BaseTool):
    retriever: WeaviateRetriever | None = None

    @classmethod
    def from_retriever_params(
            cls,
            connection_params: ConnectionParams,
            collection_name: str,
            k: int,
            embeddings: Embeddings,
            format_properties_func: Callable[[list[Property]], str],
            target_vector: str | list[str] | None = None
    ) -> BaseWeaviateRetrieverTool:
        return cls(
            retriever=WeaviateRetriever(
                connection_params=connection_params,
                k=k,
                embeddings=embeddings,
                format_properties_func=format_properties_func,
                target_vector=target_vector,
                collection_name=collection_name
            )
        )

    def _run(self, query: str) -> str:
        logger.info("---RETRIEVE FROM WEAVIATE---")
        documents = self.retriever.invoke(query)
        return format_documents(documents)

    async def _arun(self, query: str) -> str:
        logger.info("---RETRIEVE FROM WEAVIATE---")
        documents = await self.retriever.ainvoke(query)
        return format_documents(documents)
