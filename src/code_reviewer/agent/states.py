from typing import Annotated, TypedDict

from collections.abc import Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from ..schemas import AgentMode


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    mode: AgentMode
