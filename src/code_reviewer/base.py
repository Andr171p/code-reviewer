from typing import Generic, TypeVar

from abc import abstractmethod

from pydantic import BaseModel


class BaseChunk(BaseModel):
    @abstractmethod
    def to_text(self) -> str:
        raise NotImplementedError


Chunk = TypeVar("Chunk", bound=BaseChunk)


class BaseTextSplitter(Generic[Chunk]):
    """Базовый класс для разбиения текстового контента на чанки"""

    @abstractmethod
    def split_text(self, text: str) -> list[Chunk]:
        """Разделяет текстовый контент на чанки"""
        raise NotImplementedError
