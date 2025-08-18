from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, START
from langgraph.graph.state import CompiledStateGraph, StateGraph

from .nodes import (
    DeveloperNode,
    assistant_node,
    code_generation_node,
    code_review_node,
    hyde_code_generation_node,
    routing_node,
)
from .states import AgentState, DeveloperState

Agent = CompiledStateGraph[AgentState]
DeveloperAgent = CompiledStateGraph[DeveloperState]


def create_agent(
        developer_agent: DeveloperAgent, checkpointer: BaseCheckpointSaver
) -> Agent:
    workflow = StateGraph(AgentState)
    # Создание вершин графа
    workflow.add_node("routing", routing_node)
    workflow.add_node("code_review", code_review_node)
    workflow.add_node("assistant", assistant_node)
    workflow.add_node("developer", DeveloperNode(developer_agent))
    # Добавление рёбер графа
    workflow.add_edge(START, "routing")
    workflow.add_edge("code_review", END)
    workflow.add_edge("assistant", END)
    workflow.add_edge("developer", END)
    # Компиляция графа
    return workflow.compile(checkpointer=checkpointer)


def create_developer_agent() -> DeveloperAgent:
    workflow = StateGraph(DeveloperState)
    # Создание вершин графа
    workflow.add_node("hyde_generation", hyde_code_generation_node)
    workflow.add_node("search", code_generation_node)
    workflow.add_node("generation", code_generation_node)
    # Добавление рёбер графа
    workflow.add_edge(START, "hyde_generation")
    workflow.add_edge("hyde_generation", "search")
    workflow.add_edge("search", "generation")
    workflow.add_edge("generation", END)
    # Компиляция графа
    return workflow.compile()
