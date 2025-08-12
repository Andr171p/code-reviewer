from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka as Depends
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph

from ..agent.states import AgentState

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("...")


@router.message(F.text)
async def chat(
    message: Message, agent: Depends[CompiledStateGraph[AgentState]]
) -> None:
    config = RunnableConfig({"configurable": {"thread_id": str(message.from_user.id)}})
    inputs = {"messages": [{"role": "human", "content": message.text}]}
    response = await agent.ainvoke(inputs, config=config)
    last_message = response["messages"][-1]
    await message.answer(last_message.content)
