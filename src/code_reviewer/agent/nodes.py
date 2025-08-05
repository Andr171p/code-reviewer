from typing import Any

from abc import ABC, abstractmethod
import logging

from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent

from .constants import ROUTING
from .states import AgentState

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


def route_node(state: AgentState) -> Command[str]:
    """Направляет к заданному агенту"""
    node = ROUTING[state["mode"]]
    logger.info("---ROUTE TO %s NODE---", node)
    return Command(goto=node)


class ReActAgentNode(BaseNode):
    def __init__(
            self, model: BaseChatModel, prompt: str, tools: list[BaseTool]
    ) -> None:
        self.react_agent = create_react_agent(
            model=model, prompt=prompt, tools=tools
        )

    async def __call__(
            self, state: AgentState, config: RunnableConfig | None = None
    ) -> dict[str, Any]:
        logger.info("---CALL REACT AGENT---")
        response = await self.react_agent.ainvoke(
            input={"messages": state["messages"]}, config=config
        )
        return {"messages": response["messages"][-1]}
