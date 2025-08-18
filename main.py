'''import asyncio
import logging

from aiogram import Bot

from src.code_reviewer.dependencies import container
from src.code_reviewer.bot.dispatcher import create_dispatcher


async def main() -> None:
    bot = await container.get(Bot)
    dp = create_dispatcher()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())'''


import asyncio
import logging

from langchain_core.runnables import RunnableConfig
from langchain_core.vectorstores import VectorStore
from langchain_core.language_models import BaseChatModel

from src.code_reviewer.dependencies import container
from src.code_reviewer.agent.workflow import Agent


async def main() -> None:
    agent = await container.get(Agent)
    vectorstore = await container.get(VectorStore)
    llm = await container.get(BaseChatModel)
    config = RunnableConfig(
        configurable={"thread_id": str(1234567890)},
    )
    while True:
        query = input("[User]: ")
        inputs = {"messages": [{"role": "human", "content": query}]}
        response = await agent.ainvoke(inputs, config=config)
        print(f"[AI]: {response["messages"][-1].content}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
