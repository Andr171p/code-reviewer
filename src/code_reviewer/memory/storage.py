import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import ValidationError
from redis.asyncio import Redis as AsyncRedis
from redisvl.exceptions import RedisVLError, SchemaValidationError
from redisvl.index import AsyncSearchIndex
from redisvl.query import VectorRangeQuery
from redisvl.query.filter import Tag
from redisvl.schema import IndexSchema
from sentence_transformers import SentenceTransformer
from ulid import ULID

from ..schemas import Memory, MemoryType
from .constants import (
    DEFAULT_USER_ID,
    DIALECT,
    DISTANCE_THRESHOLD,
    LIMIT,
    MEMORY_SCHEMA_YML,
    MOSCOW_TZ,
    NUM_RESULTS,
)

logger = logging.getLogger(__name__)


class RedisLongTermMemory:
    def __init__(self, client: AsyncRedis, vectorizer: SentenceTransformer) -> None:
        self.client = client
        self.vectorizer = vectorizer
        self.schema = IndexSchema.from_yaml(MEMORY_SCHEMA_YML)

    def _get_or_create_index(self) -> AsyncSearchIndex:
        try:
            memory_index = AsyncSearchIndex(
                schema=self.schema, redis_client=self.client, validate_on_load=True
            )
            memory_index.create(overwrite=False)
        except SchemaValidationError:
            logger.exception("Error creating schema: {e}")
        else:
            return memory_index

    async def similar_memory_exists(
        self, memory: Memory, distance_threshold: float = DISTANCE_THRESHOLD
    ) -> bool:
        memory_index = self._get_or_create_index()
        filters = (Tag("user_id") == memory.user_id) & (Tag("memory_type") == memory.memory_type)
        if memory.thread_id:
            filters &= Tag("thread_id") == memory.thread_id
        content_vector = self.vectorizer.embed(memory.content)
        vector_query = VectorRangeQuery(
            vector=content_vector,
            num_results=NUM_RESULTS,
            vector_field_name="embedding",
            filter_expression=filters,
            distance_threshold=distance_threshold,
            return_fields=["id"],
        )
        results = await memory_index.query(vector_query)
        return bool(results)

    async def store_memory(self, memory: Memory) -> None:
        memory_index = self._get_or_create_index()
        memory_exists = await self.similar_memory_exists(memory)
        if memory_exists:
            return
        embedding = self.vectorizer.encode(memory.content)
        memory_data: dict[str, str] = {
            "user_id": memory.user_id,
            "content": memory.content,
            "memory_type": memory.memory_type.value,
            "metadata": memory.metadata,
            "created_at": datetime.now(tz=ZoneInfo(MOSCOW_TZ)).isoformat(),
            "embedding": embedding.tolist(),
            "memory_id": str(ULID()),
            "thread_id": memory.thread_id,
        }
        try:
            await memory_index.load([memory_data])
        except (SchemaValidationError, RedisVLError):
            logger.exception("Error storing memory: {e}")

    async def retrieve_memories(
        self,
        query: str,
        distance_threshold: float = DISTANCE_THRESHOLD,
        limit: int = LIMIT,
        **kwargs,
    ) -> list[Memory]:
        user_id: str = kwargs.get("user_id", DEFAULT_USER_ID)
        thread_id: str | None = kwargs.get("thread_id")
        memory_type: MemoryType | list[MemoryType] | None = kwargs.get("memory_type")
        memory_index = self._get_or_create_index()
        embedding = self.vectorizer.encode(query)
        vector_query = VectorRangeQuery(
            vector=embedding.tolist(),
            return_fields=[
                "content",
                "memory_type",
                "metadata",
                "created_at",
                "memory_id",
                "thread_id",
                "user_id",
            ],
            num_results=limit,
            vector_field_name="embedding",
            dialect=DIALECT,
            distance_threshold=distance_threshold,
        )
        base_filter = [f"@user_id:{{{user_id}}}"]
        if memory_type:
            if isinstance(memory_type, list):
                base_filter.append(f"@memory_type:{{{'|'.join(memory_type)}}}")
            else:
                base_filter.append(f"@memory_type:{{{memory_type.value}}}")
        if thread_id:
            base_filter.append(f"@thread_id:{{{thread_id}}}")
        vector_query.set_filter(" ".join(base_filter))
        results = await memory_index.query(vector_query)
        memories: list[Memory] = []
        for result in results:
            try:
                memories.append(Memory(**result))
            except ValidationError:
                logger.exception("Error parsing memory: {e}")
        return memories
