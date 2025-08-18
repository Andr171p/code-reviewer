from typing import Annotated, TypedDict

from collections.abc import Sequence

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """Основное состояние AI агента"""
    messages: Annotated[Sequence[BaseMessage], add_messages]


class DeveloperState(TypedDict):
    """Состояние агента 1С разработчика для генерации кода"""
    query: str
    hypothetical_code: str
    search_result: list[Document]
    generated_code: str
