from typing import Any, Literal

import logging
from abc import ABC, abstractmethod

from langchain_core.runnables import RunnableConfig
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStore
from langgraph.types import Command
from pydantic import BaseModel, Field

from .states import AgentState, DeveloperState
from .prompts import ROUTE_PROMPT, DEVELOPER_PROMPT
from .utils import (
    create_llm_chain_with_structured_output,
    create_rag_chain,
    create_llm_chain,
    format_documents
)
from ..constants import TOP_N

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


class HYDECodeGenerationNode(BaseNode):
    def __init__(self, model: BaseChatModel) -> None:
        self.llm_chain = create_llm_chain(
            prompt=..., llm=model
        )

    async def __call__(
            self, state: DeveloperState, config: RunnableConfig | None = None
    ) -> DeveloperState:
        logger.info("---GENERATE HYPOTHETICAL CODE---")
        hyde_code = await self.llm_chain.ainvoke({"query": state["user_query"]})
        return {"hyde_code": hyde_code}


class CodeSearchNode(BaseNode):
    def __init__(self, vectorstore: VectorStore) -> None:
        self.vectorstore = vectorstore

    async def __call__(
            self, state: DeveloperState, config: RunnableConfig | None = None
    ) -> DeveloperState:
        logger.info("---CODE SEARCH---")
        documents = await self.vectorstore.asimilarity_search(
            state["hyde_code"], k=TOP_N
        )
        return {"searched_documents": format_documents(documents)}


class CodeGenerationNode(BaseNode):
    def __init__(self, vectorstore: VectorStore, model: BaseChatModel) -> None:
        self.rag_chain = create_rag_chain(
            vectorstore=vectorstore, prompt=..., llm=model
        )

    async def __call__(
            self, state: DeveloperState, config: RunnableConfig | None = None
    ) -> DeveloperState:
        logger.info("---GENERATE CODE---")
        generated_code = await self.rag_chain.ainvoke({"query": state["user_query"]})


class DeveloperNode(BaseNode):
    def __init__(
            self, vectorstore: VectorStore, model: BaseChatModel
    ) -> None:
        self.rag_chain = create_rag_chain(
            vectorstore=vectorstore,
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


class CodeReviewerNode(BaseNode):
    def __init__(
            self, vectorstore: VectorStore, model: BaseChatModel
    ) -> None:
        self.rag_chain = create_rag_chain(
            vectorstore=vectorstore,
            prompt=DEVELOPER_PROMPT,
            llm=model
        )

    async def __call__(
            self, state: AgentState, config: RunnableConfig | None = None
    ) -> AgentState:
        logger.info("---CALL CODE-REVIEWER---")
        last_message = state["messages"][-1]
        message = await self.rag_chain.ainvoke(last_message.content)
        return {"messages": [message]}


class DocumentationAssistantNode(BaseNode):
    def __init__(
            self, vectorstore: VectorStore, model: BaseChatModel
    ) -> None:
        self.rag_chain = create_rag_chain(
            vectorstore=vectorstore,
            prompt=DEVELOPER_PROMPT,
            llm=model
        )

    async def __call__(
            self, state: AgentState, config: RunnableConfig | None = None
    ) -> AgentState:
        logger.info("---CALL DOCUMENTATION ASSISTANT---")
        last_message = state["messages"][-1]
        message = await self.rag_chain.ainvoke(last_message.content)
        return {"messages": [message]}
