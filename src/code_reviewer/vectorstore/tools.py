from __future__ import annotations

import logging

from langchain_core.tools import BaseTool, ArgsSchema
from pydantic import BaseModel, Field

from ..base import BaseVectorStore
from ..utils import run_async, format_documents

DISTANCE_THRESHOLD = 0.3
MIN_DISTANCE = 0.1
MAX_DISTANCE = 1
LIMIT = 5

logger = logging.getLogger(__name__)


class SearchQueryArgsSchema(BaseModel):
    query: str = Field(description="Запрос для поиска")
    distance_threshold: float = Field(
        default=DISTANCE_THRESHOLD,
        ge=MIN_DISTANCE,
        le=MAX_DISTANCE,
        description="Задаёт строгость поиска"
    )
    limit: int = Field(
        default=LIMIT, description="Количество элементов, которое нужно найти"
    )


class SimilaritySearchTool(BaseTool):
    name: str = "similarity_search_tool"
    description: str = """Инструмент поиска информации для 1С разработчика,
    может найти: модули с .bsl кодом, примеры из документации, лучшие практики и многое другое.
    """
    args: ArgsSchema | None = SearchQueryArgsSchema

    vectorstore: BaseVectorStore | None = None

    @classmethod
    def from_vectorstore(cls, vectorstore: BaseVectorStore) -> SimilaritySearchTool:
        return cls(vectorstore=vectorstore)

    def _run(self, query: str) -> str:
        return run_async(self._arun(query))

    async def _arun(
            self, query: str,
            distance_threshold: float = DISTANCE_THRESHOLD,
            limit: int = LIMIT
    ) -> str:
        logger.info("---SIMILARITY SEARCH---")
        documents = await self.vectorstore.similarity_search(
            query, distance_threshold, limit
        )
        return format_documents(documents)
