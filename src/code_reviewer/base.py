from typing import Generic, TypeVar

from abc import ABC, abstractmethod

from pydantic import BaseModel

from .schemas import Memory, Document


class BaseChunk(BaseModel):
    @abstractmethod
    def to_text(self) -> str:
        raise NotImplementedError


C = TypeVar("C", bound=BaseChunk)


class BaseTextSplitter(Generic[C]):
    """Базовый класс для разбиения текстового контента на чанки"""

    @abstractmethod
    def split_text(self, text: str) -> list[C]:
        """Разделяет текстовый контент на чанки"""
        raise NotImplementedError


class BaseMemoryStore(ABC):
    """Базовый класс для управления долгосрочной памятью"""

    @abstractmethod
    async def store_memory(self, memory: Memory) -> None:
        """Сохраняет в долгосрочную память"""
        raise NotImplementedError

    @abstractmethod
    async def retrieve_memories(
            self,
            query: str,
            distance_threshold: float,
            limit: int,
            **kwargs
    ) -> list[Memory]:
        """Извлекает воспоминания по запросу"""
        raise NotImplementedError


class BaseVectorStore(ABC):
    @abstractmethod
    async def similarity_search(
            self, query: str, distance_threshold: float, limit: int, **kwargs
    ) -> list[Document]:
        pass

    @abstractmethod
    async def add(self, document: list[Document], **kwargs) -> None:
        pass
