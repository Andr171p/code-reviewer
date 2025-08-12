from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka as Depends
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.message import MessagesState

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("Бот запущен")


@router.message(F.text)
async def chat(
    message: Message, agent: Depends[CompiledStateGraph[MessagesState]]
) -> None:
    config = RunnableConfig(configurable={"thread_id": str(1234567890)})
    inputs = {"messages": [{"role": "human", "content": message.text}]}
    response = await agent.ainvoke(inputs, config=config)
    last_message = response["messages"][-1]
    await message.answer(last_message.content)


# https://github.com/BlizD/Tasks/blob/develope/src/cf/BusinessProcesses/%D0%97%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5/Ext/ObjectModule.bsl