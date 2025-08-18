from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from .agent import run_agent

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("Бот запущен")


@router.message(F.text)
async def chat(message: Message) -> None:
    response = await run_agent(
        chat_id=str(message.from_user.id), user_prompt=message.text
    )
    await message.answer(response)
