from typing import Generic, TypeVar

from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class CRUDRepository(Generic[T]):
    async def create(self, model: T) -> T: pass

    async def read(self, id: UUID) -> T | None: pass

    async def update(self, id: UUID, **kwargs) -> T | None: pass

    async def delete(self, id: UUID) -> bool: pass
