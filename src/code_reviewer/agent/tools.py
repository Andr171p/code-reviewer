from __future__ import annotations

import logging

from langchain_core.embeddings import Embeddings
from langchain_core.tools import ArgsSchema, BaseTool
from langchain_pinecone import PineconeVectorStore
from pydantic import BaseModel, Field

from ..utils import run_async
from .utils import format_documents

logger = logging.getLogger(__name__)

TOP_N = 7


class SearchInput(BaseModel):
    query: str = Field(..., description="Запрос для поиска")
    index_name: str = Field(
        ..., description="Название индекса в котором нужно выполнить поиск"
    )
    top_n: int = Field(
        default=TOP_N, description="Количество извлекаемых элементов"
    )


class QuerySearchTool(BaseTool):
    name: str = "QuerySearch"
    description: str = """Инструмент для векторного поиска.
    """
    args_schema: ArgsSchema | None = SearchInput
    embeddings: Embeddings | None = None
    pinecone_api_key: str | None = None

    @classmethod
    def from_pinecone(
            cls, embeddings: Embeddings, pinecone_api_key: str
    ) -> QuerySearchTool:
        return cls(embeddings=embeddings, pinecone_api_key=pinecone_api_key)

    def _run(
            self, query: str, index_name: str, top_n: int
    ) -> str:
        return run_async(self._arun(query, index_name, top_n))

    async def _arun(
            self, query: str, index_name: str, top_n: int = TOP_N
    ) -> str:
        logger.info("---SEARCH FROM %s---", self.index_name.upper())
        vectorstore = PineconeVectorStore(
            embedding=self.embeddings,
            index_name=index_name,
            pinecone_api_key=self.api_key
        )
        documents = vectorstore.similarity_search(query, k=TOP_N)
        return format_documents(documents)
