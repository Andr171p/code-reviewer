from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import END, START, CompiledStateGraph, StateGraph

from .nodes import ReviewerNode
from .states import AgentState


def build_graph(
    reviewer: ReviewerNode, checkpointer: BaseCheckpointSaver
) -> CompiledStateGraph[AgentState]:
    workflow = StateGraph(AgentState)
    workflow.add_node("reviewer", reviewer)
    workflow.add_edge(START, "reviewer")
    workflow.add_edge("reviewer", END)
    return workflow.compile(checkpointer=checkpointer)
