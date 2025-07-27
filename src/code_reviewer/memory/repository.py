import logging

from redis.asyncio import Redis as AsyncRedis
from redisvl.index import AsyncSearchIndex
from redisvl.exceptions import SchemaValidationError
from redisvl.utils.vectorize import HFTextVectorizer

from .schemas import memory_schema
from .models import MemoryType

logger = logging.getLogger(__name__)


class RedisLongTermMemoryRepository:
    def __init__(self, redis_client: AsyncRedis) -> None:
        self.redis_client = redis_client

    async def _create_index(self) -> ...:
        try:
            long_term_memory_index = AsyncSearchIndex(
                schema=memory_schema,
                redis_client=self.redis_client,
                validate_on_load=True
            )
            await long_term_memory_index.create(overwrite=True)
        except SchemaValidationError as e:
            ...

    async def similarity_search(
            content: str,
            memory_type: MemoryType,
            user_id: str = ...,
            thread_id: str | None = None,
            distance_threshold: float = 0.1,
    ) -> bool:
        ...
