from typing import Any

import logging
from abc import ABC, abstractmethod

from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import RunnableConfig
from langchain_core.vectorstores import VectorStore
from langgraph.prebuilt import create_react_agent

from .prompts import REVIEWER_PROMPT
from .states import AgentState
from .tools import ITSSearchTool

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


class ReviewerNode(BaseNode):
    def __init__(self, vectorstore: VectorStore, model: BaseChatModel) -> None:
        self.agent = create_react_agent(
            tools=[ITSSearchTool.from_vectorstore(vectorstore)],
            prompt=REVIEWER_PROMPT,
            model=model,
        )

    async def __call__(
        self, state: AgentState, config: RunnableConfig | None = None  # noqa: ARG002
    ) -> AgentState:
        logger.info("---ASK REVIEWER---")
        last_message = state["messages"][-1]
        inputs = {"messages": [{"role": "human", "content": last_message.content}]}
        response = await self.agent.ainvoke(inputs)
        return {"messages": [response["messages"][-1]]}
