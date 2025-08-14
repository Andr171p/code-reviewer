from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka as Depends
from langchain_core.runnables import RunnableConfig

from ..agent.workflow import Agent
from ..utils import split_text

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("Бот запущен")


@router.message(F.text)
async def chat(message: Message, agent: Depends[Agent]) -> None:
    config = RunnableConfig(configurable={"thread_id": str(message.from_user.id)})
    inputs = {"messages": [{"role": "human", "content": message.text}]}
    response = await agent.ainvoke(inputs, config=config)
    last_message = response["messages"][-1]
    texts = split_text(last_message.content)
    for text in texts:
        await message.answer(text)
