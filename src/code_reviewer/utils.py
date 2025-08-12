from typing import Any, TypeVar

import asyncio
from collections.abc import Coroutine

T = TypeVar("T")


def run_async[T](coroutine: Coroutine[Any, Any, T]) -> T:
    """
    Выполняет асинхронную функцию синхронно.

    :param coroutine: Асинхронная функция для запуска.
    :return: T результат выполнения асинхронной функции.
    """
    event_loop = asyncio.get_event_loop()
    return event_loop.run_until_complete(coroutine)
