from typing import Any, TypeVar

import asyncio
from collections.abc import Coroutine

from .constants import MAX_TELEGRAM_MESSAGE_LENGTH

T = TypeVar("T")


def run_async[T](coroutine: Coroutine[Any, Any, T]) -> T:
    """
    Выполняет асинхронную функцию синхронно.

    :param coroutine: Асинхронная функция для запуска.
    :return: T результат выполнения асинхронной функции.
    """
    event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(coroutine)


def split_text(text: str) -> list[str]:
    """Разбивает большое сообщение на части,
    не превышающие максимальный размер сообщения в Telegram.

    :param text: Исходный текст сообщения
    :return: Список частей текста, каждая не длиннее MAX_TELEGRAM_MESSAGE_LENGTH
    """
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + MAX_TELEGRAM_MESSAGE_LENGTH
        chunks.append(text[start:end])
        start = end
    return chunks
