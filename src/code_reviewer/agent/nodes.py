from typing import Any

from abc import ABC, abstractmethod
import logging

from langgraph.types import Command

from .constants import ROUTING
from .states import AgentState

logger = logging.getLogger(__name__)


class BaseNode(ABC):
    """Базовый класс для реализации вершины графа"""
    @abstractmethod
    async def __call__(self, state: dict[str, Any]) -> dict[str, Any]:
        """Выполняет логику заданную в вершине (узле) графа.

        :param state: Накопленное FSM состояние графа.
        :return Обновлённое состояние графа.
        """
        raise NotImplementedError


def route_node(state: AgentState) -> Command[str]:
    """Направляет к заданному агенту"""
    node = ROUTING[state["mode"]]
    logger.info("---ROUTE TO %s NODE---", node)
    return Command(goto=node)
