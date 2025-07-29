from typing import cast

from functools import cached_property

from langchain_core.tools import BaseTool, BaseToolkit
from pydantic import ConfigDict, Field
from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from redisvl.utils.vectorize import BaseVectorizer

from ..memory import AsyncRedisMemoryStorage, BaseMemoryTool, RedisMemoryStorage, memory_schema
from .tools import RetrieveMemoriesTool, StoreMemoryTool


class RedisLongTermMemoryToolkit(BaseToolkit):
    """Toolkit для работы с долгосрочной памятью используя Redis"""
    client: Redis = Field(exclude=True)
    async_client: AsyncRedis = Field(exclude=True)
    vectorizer: BaseVectorizer = Field(exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @cached_property
    def storage(self) -> RedisMemoryStorage:
        return RedisMemoryStorage(
            client=self.client,
            schema=memory_schema,
            vectorizer=self.vectorizer
        )

    @cached_property
    def async_storage(self) -> AsyncRedisMemoryStorage:
        return AsyncRedisMemoryStorage(
            client=self.client,
            schema=memory_schema,
            vectorizer=self.vectorizer
        )

    def get_tools(self) -> list[BaseTool]:
        tool_classes: list[type[BaseMemoryTool]] = [
            StoreMemoryTool, RetrieveMemoriesTool
        ]
        tools: list[BaseMemoryTool] = [
            tool_class.from_storage(
                storage=self.storage, async_storage=self.async_storage
            )
            for tool_class in tool_classes
        ]
        return cast(list[BaseTool], tools)
