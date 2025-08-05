from __future__ import annotations

from typing import Any

import logging

from langchain_core.tools import BaseTool, ToolException, ArgsSchema
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field

from ..base import BaseMemoryStore
from ..schemas import MemoryType, Memory
from ..utils import run_async
from .constants import LIMIT

DISTANCE_THRESHOLD = 0.3

logger = logging.getLogger(__name__)


class BaseMemoryTool(BaseTool):
    """Базовый класс для инструментов работающих с долгосрочной памятью"""
    storage: BaseMemoryStore

    @classmethod
    def from_storage(
            cls, storage: BaseMemoryStore | None = None,
    ) -> BaseMemoryTool:
        return cls(storage=storage)

    def _run(self, *args, **kwargs) -> Any:
        return run_async(self._arun(*args, **kwargs))

    async def _arun(self, *args, **kwargs) -> Any:
        """Асинхронный вызов инструмента."""
        raise NotImplementedError


class MemoryArgsSchema(BaseModel):
    content: str = Field(description="Информация которую нужно сохранить")
    memory_type: MemoryType = Field(description="Тип памяти")
    metadata: dict[str, str] = Field(
        description="Дополнительные метаданные, которые могут пригодится"
    )


class StoreMemoryTool(BaseMemoryTool):
    name: str = "store_memory_tool"
    description: str = """Храни долговременную память в системе.

    Используй этот инструмент, чтобы сохранить важную информацию о предпочтениях пользователя,
    опыт или общие знания, которые могут быть полезны в будущем.
    """
    args_schema: ArgsSchema | None = MemoryArgsSchema

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
        memory = Memory(
            user_id=user_id,
            thread_id=thread_id,
            content=content,
            memory_type=memory_type,
            metadata=metadata,
        )
        try:
            await self.storage.store_memory(memory)
            return f"Успешно сохранено {memory_type} в память: {content}"
        except Exception as e:
            raise ToolException(f"Ошибка при сохранении памяти: {e}") from e


class QueryMemoryArgsSchema(BaseModel):
    query: str = Field(description="Запрос для извлечения памяти")
    memory_type: list[MemoryType] = Field(description="Типы памяти")
    limit: int = Field(default=LIMIT, description="Лимит извлекаемых воспоминаний")


class RetrieveMemoriesTool(BaseMemoryTool):
    name: str = "retrieve_memory_tool"
    description: str = """Получение долговременной памяти, относящейся к вопросу.

    Используй этот инструмент для доступа к ранее сохраненной информации о пользователе.
    предпочтения, опыт или общие знания.
    """
    args_schema: ArgsSchema | None = QueryMemoryArgsSchema

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
            stored_memories = await self.storage.retrieve_memories(
                query=query,
                memory_type=memory_type,
                user_id=user_id,
                limit=limit,
                distance_threshold=DISTANCE_THRESHOLD
            )
            response: list[str] = []
            if not stored_memories:
                return "Соответствующих воспоминаний не найдено."
            response.append("Долговременная память:")
            for stored_memory in stored_memories:
                response.append(f"- [{stored_memory.memory_type}] {stored_memory.content}")
            return "\n".join(response)
        except Exception as e:
            raise ToolException(f"Ошибка при извлечении памяти: {e}") from e
