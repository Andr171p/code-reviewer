from __future__ import annotations

import logging

from langchain_core.tools import ArgsSchema, BaseTool
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel, Field

from ..utils import run_async
from .utils import format_documents

logger = logging.getLogger(__name__)

TOP_N = 7


class SearchInput(BaseModel):
    query: str = Field(..., description="Запрос для поиска")


class ITSSearchTool(BaseTool):
    name: str = "ITSRetriever"
    description: str = """Инструмент для поиска полезной информации, лучших практик
    по 1С разработке с сайта 1c.its.ru.
    """
    args_schema: ArgsSchema | None = SearchInput
    vectorstore: VectorStore | None = None

    @classmethod
    def from_vectorstore(cls, vectorstore: VectorStore) -> ITSSearchTool:
        return cls(vectorstore=vectorstore)

    def _run(self, query: str) -> str:
        return run_async(self._arun(query))

    async def _arun(self, query: str) -> str:
        logger.info("---SEARCH FROM ITS---")
        documents = self.vectorstore.similarity_search(query, k=TOP_N)
        return format_documents(documents)
