from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from weaviate.classes.config import Property

import logging

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import ArgsSchema, ToolException
from pydantic import BaseModel, Field

from .constants import FORMATED_MODULE_PROPERTIES, FORMATED_DOCS_PROPERTIES
from ..memory import BaseRedisMemoryTool, Memory, MemoryType
from ..vectorstore import BaseWeaviateSearchTool

DISTANCE_THRESHOLD = 0.3
LIMIT = 5

logger = logging.getLogger(__name__)


class StoreMemoryTool(BaseRedisMemoryTool):
    name: str = "store_memory_tool"
    description: str = """Храни долговременную память в системе.
    
    Используй этот инструмент, чтобы сохранить важную информацию о предпочтениях пользователя,
    опыт или общие знания, которые могут быть полезны в будущем.
    """
    args_schema: ArgsSchema | None = Memory

    def _run(
            self,
            content: str,
            memory_type: MemoryType,
            metadata: dict[str, str] | None = None,
            config: RunnableConfig | None = None
    ) -> str:
        logger.info("---STORE MEMORY---")
        config = config or RunnableConfig()
        user_id = config.get("user_id", "")
        thread_id = config.get("thread_id")
        try:
            self.storage.store_memory(
                content=content,
                memory_type=memory_type,
                user_id=user_id,
                thread_id=thread_id,
                metadata=metadata
            )
            return f"Успешно сохранено {memory_type} в память: {content}"
        except Exception as e:
            raise ToolException(f"Ошибка при сохранении памяти: {e}") from e

    async def _arun(
            self,
            content: str,
            memory_type: MemoryType,
            metadata: dict[str, str] | None = None,
            config: RunnableConfig | None = None,
    ) -> str:
        logger.info("---STORE MEMORY---")
        config = config or RunnableConfig()
        user_id = config.get("user_id", "")
        thread_id = config.get("thread_id")
        try:
            await self.async_storage.store_memory(
                content=content,
                memory_type=memory_type,
                user_id=user_id,
                thread_id=thread_id,
                metadata=metadata
            )
            return f"Успешно сохранено {memory_type} в память: {content}"
        except Exception as e:
            raise ToolException(f"Ошибка при сохранении памяти: {e}") from e


class RetrieveMemoriesArgsSchema(BaseModel):
    query: str = Field(description="Запрос для извлечения памяти")
    memory_type: list[MemoryType] = Field(description="Типы памяти")
    limit: int = Field(default=LIMIT, description="Лимит извлекаемых воспоминаний")


class RetrieveMemoriesTool(BaseRedisMemoryTool):
    name: str = "retrieve_memory_tool"
    description: str = """Получение долговременной памяти, относящейся к вопросу.
    
    Используй этот инструмент для доступа к ранее сохраненной информации о пользователе.
    предпочтения, опыт или общие знания.
    """
    args_schema: ArgsSchema | None = RetrieveMemoriesArgsSchema

    def _run(
            self,
            query: str,
            memory_type: list[MemoryType],
            limit: int = LIMIT,
            config: RunnableConfig | None = None
    ) -> str:
        logger.info("---RETRIEVE MEMORIES---")
        config = config or RunnableConfig()
        user_id = config.get("user_id", "")
        try:
            stored_memories = self.storage.retrieve(
                query=query,
                memory_type=memory_type,
                user_id=user_id,
                limit=limit,
                distance_threshold=DISTANCE_THRESHOLD
            )
            response: list[str] = []
            if not stored_memories:
                return "Соответствующей памяти не найдено."
            response.append("Долговременная память:")
            for stored_memory in stored_memories:
                response.append(f"- [{stored_memory.memory_type}] {stored_memory.content}")
            return "\n".join(response)
        except Exception as e:
            raise ToolException(f"Ошибка при извлечении памяти: {e}") from e

    async def _arun(
            self,
            query: str,
            memory_type: list[MemoryType],
            limit: int = LIMIT,
            config: RunnableConfig | None = None
    ) -> str:
        logger.info("---RETRIEVE MEMORIES---")
        config = config or RunnableConfig()
        user_id = config.get("user_id", "")
        try:
            stored_memories = await self.async_storage.retrieve(
                query=query,
                memory_type=memory_type,
                user_id=user_id,
                limit=limit,
                distance_threshold=DISTANCE_THRESHOLD
            )
            response: list[str] = []
            if not stored_memories:
                return "Соответствующей памяти не найдено."
            response.append("Долговременная память:")
            for stored_memory in stored_memories:
                response.append(f"- [{stored_memory.memory_type}] {stored_memory.content}")
            return "\n".join(response)
        except Exception as e:
            raise ToolException(f"Ошибка при извлечении памяти: {e}") from e


class SearchArgsSchema(BaseModel):
    query: str = Field(description="Запрос для поиска")
    limit: int = Field(default=LIMIT, description="Количество поисковых результатов")


class SearchModulesTool(BaseWeaviateSearchTool):
    name: str = "search_modules_tool"
    description: str = """Используй этот инструмент для поиска примеров кода из bsl модулей
    """
    args_schema: ArgsSchema | None = SearchArgsSchema
    collection_name: str = "Modules"

    def _format_properties(self, properties: list[Property]) -> str:
        return FORMATED_MODULE_PROPERTIES.format(*properties)


class SearchDocsTool(BaseWeaviateSearchTool):
    name: str = "search_docs_tool"
    description: str = "используй этот инструмент для поиска информации книгах и документации по 1С"
    args_schema: ArgsSchema | None = SearchArgsSchema
    collection_name: str = "Docs"

    def _format_properties(self, properties: list[Property]) -> str:
        return FORMATED_DOCS_PROPERTIES.format(*properties)
