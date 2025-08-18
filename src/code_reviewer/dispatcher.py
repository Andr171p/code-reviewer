from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dishka.integrations.aiogram import setup_dishka

from src.code_reviewer.dependencies import container
from src.code_reviewer.handlers import router


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(router)
    setup_dishka(container=container, router=dispatcher, auto_inject=True)
    return dispatcher
