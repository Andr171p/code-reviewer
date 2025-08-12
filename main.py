import asyncio

from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import MessagesState

from src.code_reviewer.dependencies import container


async def main() -> None:
    agent = await container.get(CompiledStateGraph[MessagesState])
    config = RunnableConfig(configurable={"thread_id": str(123)})
    while True:
        query = input("[User]: ")
        inputs = {"messages": [{"role": "human", "content": query}]}
        async for chunk in agent.astream(inputs, config=config):
            print(chunk)
            print("\n\n")


if __name__ == "__main__":
    asyncio.run(main())
