from typing import Any

import logging
from abc import ABC, abstractmethod

from langchain_core.runnables import RunnableConfig

logger = logging.getLogger(__name__)


class BaseNode(ABC):
    """Базовый класс для реализации вершины графа"""

    @abstractmethod
    async def __call__(
        self, state: dict[str, Any], config: RunnableConfig | None = None
    ) -> dict[str, Any]:
        """Выполняет логику заданную в вершине (узле) графа.

        :param state: Накопленное FSM состояние графа.
        :param config: Конфиг заданный при запуске агента.
        :return Обновлённое состояние графа.
        """
        raise NotImplementedError
