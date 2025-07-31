import asyncio
import logging

from src.code_reviewer.agent.workflow import chat

query = """Привет, я пишу проект который интегрируется с внешним api, как я могу это реализовать в 1С
"""


async def main() -> None:
    await chat(query)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

