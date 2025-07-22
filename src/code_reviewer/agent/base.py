from typing import TypedDict

from abc import ABC, abstractmethod


class BaseNode(ABC):
    @abstractmethod
    async def __call__(self, state: TypedDict) -> TypedDict: pass
