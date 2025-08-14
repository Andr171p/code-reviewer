from typing import Any, Literal

import logging
from abc import ABC, abstractmethod

from langchain_core.runnables import RunnableConfig
from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langgraph.types import Command
from langgraph.graph import START, END
from pydantic import BaseModel, Field

from .states import AgentState
from .prompts import ROUTE_PROMPT, DEVELOPER_PROMPT
from .utils import create_llm_chain_with_structured_output, create_rag_chain

ROUTING = Literal[""]

logger = logging.getLogger(__name__)


class BaseNode(ABC):
    """Базовый класс для реализации вершины графа"""

    @abstractmethod
    async def __call__(
        self, state: dict[str, Any], config: RunnableConfig | None = None
    ) -> dict[str, Any] | Command:
        """Выполняет логику заданную в вершине (узле) графа.

        :param state: Накопленное FSM состояние графа.
        :param config: Конфиг заданный при запуске агента.
        :return Обновлённое состояние графа.
        """
        raise NotImplementedError


class RoutingResult(BaseModel):
    node: ROUTING = Field(description="Агент к которому нужно перенаправить")


class RoutingNode(BaseNode):
    def __init__(self, model: BaseChatModel) -> None:
        self.chain = create_llm_chain_with_structured_output(
            output_schema=RoutingResult,
            prompt=ROUTE_PROMPT,
            llm=model
        )

    async def __call__(
            self, state: AgentState, config: RunnableConfig | None = None
    ) -> Command[ROUTING]:
        last_message = state["messages"][-1]
        routing_result = await self.chain.ainvoke({"query": last_message.content})
        logger.info("---ROUTE TO %s---", routing_result.node)
        return Command(goto=routing_result.node)


class DeveloperNode(BaseNode):
    def __init__(
            self, retriever: BaseRetriever, model: BaseChatModel
    ) -> None:
        self.rag_chain = create_rag_chain(
            retriever=retriever,
            prompt=DEVELOPER_PROMPT,
            llm=model
        )

    async def __call__(
            self, state: AgentState, config: RunnableConfig | None = None
    ) -> AgentState:
        logger.info("---CALL DEVELOPER---")
        last_message = state["messages"][-1]
        message = await self.rag_chain.ainvoke(last_message.content)
        return {"messages": [message]}
