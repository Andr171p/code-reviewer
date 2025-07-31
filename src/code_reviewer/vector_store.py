import asyncio
import logging

from src.code_reviewer.agent.workflow import chat

query = "О чем мы говорили"


async def main() -> None:
    await chat(query)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

