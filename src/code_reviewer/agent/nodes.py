import logging
from enum import StrEnum

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.vectorstores import VectorStore
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command
from pydantic import BaseModel, Field

from ..constants import TOP_N
from .prompts import (
    ASSISTANT_PROMPT,
    CODE_REVIEW_PROMPT,
    DEVELOPER_PROMPT,
    HYPOTHETICAL_CODE_GENERATION_PROMPT,
    ROUTE_PROMPT,
)
from .states import AgentState, DeveloperState
from .utils import (
    create_chain,
    create_chain_with_structured_output,
    create_rag_chain,
    format_documents,
)

logger = logging.getLogger(__name__)


class Nodes(StrEnum):
    DEVELOPER = "developer"
    CODE_REVIEW = "code_review"
    ASSISTANT = "assistant"


class RoutingResult(BaseModel):
    next_node: Nodes = Field(description="Агент к которому нужно перенаправить")


async def routing_node(state: AgentState, config: RunnableConfig | None = None) -> Command[Nodes]:
    """Выполняет маршрутизацию между агентами по запросу пользователя"""
    llm: BaseChatModel = config.get("dependencies").get("llm")
    llm_chain = create_chain_with_structured_output(
        output_type=RoutingResult,
        prompt=ROUTE_PROMPT,
        llm=llm,
    )
    last_message = state["messages"][-1]
    result = await llm_chain.ainvoke({"query": last_message.content})
    logger.info("---ROUTE TO %s---", result.next_node.upper())
    return Command(goto=result.next_node)


async def hyde_code_generation_node(
    state: DeveloperState, config: RunnableConfig | None = None
) -> dict[str, str]:
    """Генерирует гипотетически возможный код по запросу пользователя"""
    logger.info("---GENERATE HYDE CODE---")
    llm: BaseChatModel = config.get("dependencies").get("llm")
    llm_chain = create_chain(prompt=HYPOTHETICAL_CODE_GENERATION_PROMPT, llm=llm)
    hypothetical_code = await llm_chain.ainvoke({"query": state["query"]})
    return {"hypothetical_code": hypothetical_code.content}


async def code_search_node(
    state: DeveloperState, config: RunnableConfig | None = None
) -> dict[str, str]:
    """Выполняет семантический поиск кода по гипотетически сгенерированному коду"""
    logger.info("---SEARCH CODE---")
    vectorstore: VectorStore = config.get("dependencies").get("vectorstore")
    documents = await vectorstore.asimilarity_search(query=state["query"], k=TOP_N)
    return {"search_results": format_documents(documents)}


async def code_generation_node(
    state: DeveloperState, config: RunnableConfig | None = None
) -> dict[str, str]:
    """Генерирует 1С код используя обогащенный контекст с примерами кода"""
    logger.info("---GENERATE CODE---")
    llm: BaseChatModel = config.get("dependencies").get("llm")
    vectorstore: VectorStore = config.get("dependencies").get("vectorstore")
    rag_chain = create_rag_chain(
        vectorstore=vectorstore,
        prompt=DEVELOPER_PROMPT.format(context=state["search_result"]),
        llm=llm
    )
    ai_message = await rag_chain.ainvoke(state["query"])
    return {"generated_code": ai_message.content}


async def code_review_node(
    state: AgentState, config: RunnableConfig | None = None
) -> dict[str, list[BaseMessage]]:
    """Производит код ревью, используя документацию"""
    logger.info("---REVIEW CODE---")
    vectorstore: VectorStore = config.get("dependencies").get("vectorstore")
    llm: BaseChatModel = config.get("dependencies").get("llm")
    rag_chain = create_rag_chain(
        vectorstore=vectorstore, prompt=CODE_REVIEW_PROMPT, llm=llm
    )
    last_message = state["messages"][-1]
    ai_message = await rag_chain.ainvoke(last_message.content)
    return {"messages": [ai_message]}


async def assistant_node(
    state: AgentState, config: RunnableConfig | None = None
) -> dict[str, list[BaseMessage]]:
    """Ассистент для ответов по 1С документации"""
    logger.info("---CALL ASSISTANT---")
    vectorstore: VectorStore = config.get("dependencies").get("vectorstore")
    llm: BaseChatModel = config.get("dependencies").get("llm")
    rag_chain = create_rag_chain(vectorstore=vectorstore, prompt=ASSISTANT_PROMPT, llm=llm)
    last_message = state["messages"][-1]
    ai_message = await rag_chain.ainvoke(last_message.content)
    return {"messages": [ai_message]}


class DeveloperNode:
    """Узел графа для работы с AI агентом 1С разработчиком"""

    def __init__(self, agent: CompiledStateGraph[DeveloperState]) -> None:
        self.agent = agent

    async def __call__(
        self, state: AgentState, config: RunnableConfig | None = None
    ) -> dict[str, list[dict[str, str]]]:
        logger.info("---CALL DEVELOPER---")
        last_message = state["messages"][-1]
        response = await self.agent.ainvoke({"query": last_message.content}, config=config)
        return {"messages": [{"role": "ai", "content": response["generated_code"]}]}
