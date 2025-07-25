from typing import Any

from abc import ABC, abstractmethod


class BaseNode(ABC):
    @abstractmethod
    async def __call__(self, state: dict[str, Any]) -> dict[str, Any]: pass
