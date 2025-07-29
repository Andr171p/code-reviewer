from __future__ import annotations

from typing import Any

from langchain_core.tools import BaseTool
from pydantic import model_validator

from .storage import AsyncRedisMemoryStorage, RedisMemoryStorage


class BaseRedisMemoryTool(BaseTool):
    """Базовый класс для инструментов работающих с памятью, используя Redis"""
    storage: RedisMemoryStorage | None = None
    async_storage: AsyncRedisMemoryStorage | None = None

    @classmethod
    def from_storage(
            cls,
            storage: RedisMemoryStorage | None = None,
            async_storage: AsyncRedisMemoryStorage | None = None
    ) -> BaseRedisMemoryTool:
        """Инициализация инструмента через уже готовое хранилище"""
        return cls(storage=storage, async_storage=async_storage)

    @model_validator(mode="before")
    def validate_storage_provided(self) -> BaseRedisMemoryTool:
        """Проверка инициализации разных типов памяти"""
        if self.storage is None and self.async_storage is None:
            raise ValueError("Either storages instances must be provided!")
        return self

    def _run(self, *args, **kwargs) -> Any:
        """Синхронный вызов инструмента."""
        raise NotImplementedError

    async def _arun(self, *args, **kwargs) -> Any:
        """Асинхронный вызов инструмента."""
        raise NotImplementedError
