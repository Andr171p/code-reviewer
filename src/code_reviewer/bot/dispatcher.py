from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dishka.integrations.aiogram import setup_dishka

from ..dependencies import container
from .handlers import chat_router, customer_router, registration_router


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_routers(registration_router, customer_router, chat_router)
    setup_dishka(container=container, router=dispatcher, auto_inject=True)
    return dispatcher
