from typing import cast

from functools import cached_property

from langchain_core.embeddings import Embeddings
from langchain_core.tools import BaseTool, BaseToolkit
from pydantic import ConfigDict, Field
from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from redisvl.utils.vectorize import BaseVectorizer
from weaviate import WeaviateAsyncClient, WeaviateClient

from ..vectorstore import BaseWeaviateSearchTool
from ..memory import AsyncRedisMemoryStorage, BaseRedisMemoryTool, RedisMemoryStorage, memory_schema
from .tools import RetrieveMemoriesTool, StoreMemoryTool, SearchModulesTool, SearchDocsTool


class RedisLongTermMemoryToolkit(BaseToolkit):
    """Toolkit для работы с долгосрочной памятью используя Redis"""
    url: str = Field(description="URL для подключения к Redis")
    vectorizer: BaseVectorizer = Field(exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @cached_property
    def storage(self) -> RedisMemoryStorage:
        return RedisMemoryStorage(
            client=Redis.from_url(self.url),
            schema=memory_schema,
            vectorizer=self.vectorizer
        )

    @cached_property
    def async_storage(self) -> AsyncRedisMemoryStorage:
        return AsyncRedisMemoryStorage(
            client=AsyncRedis.from_url(self.url),
            schema=memory_schema,
            vectorizer=self.vectorizer
        )

    def get_tools(self) -> list[BaseTool]:
        tool_classes: list[type[BaseRedisMemoryTool]] = [
            StoreMemoryTool, RetrieveMemoriesTool
        ]
        tools: list[BaseRedisMemoryTool] = [
            tool_class.from_storage(
                storage=self.storage, async_storage=self.async_storage
            )
            for tool_class in tool_classes
        ]
        return cast(list[BaseTool], tools)


class WeaviateSearchToolkit(BaseToolkit):
    """Toolkit для поиска по индексам weaviate"""
    connection_params: dict[str, str | int] = Field(
        description="Параметры для подключения в Weaviate"
    )
    embeddings: Embeddings = Field(exclude=True)

    @cached_property
    def client(self) -> WeaviateClient:
        return WeaviateClient(**self.connection_params)

    @cached_property
    def async_client(self) -> WeaviateAsyncClient:
        return WeaviateAsyncClient(**self.connection_params)

    def get_tools(self) -> list[BaseTool]:
        tool_classes: list[type[BaseWeaviateSearchTool]] = [
            SearchDocsTool,
            SearchModulesTool
        ]
        tools: list[BaseWeaviateSearchTool] = [
            tool_class.from_client(
                client=self.client,
                async_client=self.async_client,
                embeddings=self.embeddings
            )
            for tool_class in tool_classes
        ]
        return cast(list[BaseTool], tools)
