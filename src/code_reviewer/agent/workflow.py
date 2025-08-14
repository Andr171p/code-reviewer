from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import START, END

from .states import AgentState
from .nodes import DeveloperNode

Agent = CompiledStateGraph[AgentState]


def build_graph(
        developer_node: DeveloperNode, checkpointer: BaseCheckpointSaver
) -> Agent:
    workflow = StateGraph(AgentState)
    # Добавление узлов (вершин) графа
    workflow.add_node("developer", developer_node)
    # Добавление рёбер графа
    workflow.add_edge(START, "developer")
    workflow.add_edge("developer", END)
    # Компиляция графа
    return workflow.compile(checkpointer=checkpointer)
