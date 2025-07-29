import logging
from datetime import datetime
from ulid import ULID

from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from redisvl.index import AsyncSearchIndex, SearchIndex
from redisvl.schema import IndexSchema
from redisvl.exceptions import SchemaValidationError
from redisvl.query import VectorRangeQuery
from redisvl.query.filter import Tag
from redisvl.utils.vectorize import BaseVectorizer

from .models import MemoryType, StoredMemory
from .constants import DIALECT, DISTANCE_THRESHOLD, NUM_RESULTS, LIMIT

logger = logging.getLogger(__name__)


class RedisMemoryStorage:
    def __init__(
            self,
            client: Redis,
            schema: IndexSchema,
            vectorizer: BaseVectorizer
    ) -> None:
        self.client = client
        self.schema = schema
        self.vectorizer = vectorizer

    def _get_or_create_index(self) -> SearchIndex:
        try:
            memory_index = SearchIndex(
                schema=self.schema,
                redis_client=self.client,
                validate_on_load=True
            )
            memory_index.create(overwrite=False)
        except SchemaValidationError as e:
            logger.exception("Error creating schema: %s", str(e))

    def similar_memory_exists(
            self,
            content: str,
            memory_type: MemoryType,
            user_id: str,
            thread_id: str | None = None,
            distance_threshold: float = DISTANCE_THRESHOLD,
    ) -> bool:
        memory_index = self._get_or_create_index()
        filters = (Tag("user_id") == user_id) & (Tag("memory_type") == memory_type)
        if thread_id:
            filters = filters & (Tag("thread_id") == thread_id)
        content_embedding = self.vectorizer.embed(content)
        vector_query = VectorRangeQuery(
            vector=content_embedding,
            num_results=NUM_RESULTS,
            vector_field_name="embedding",
            filter_expression=filters,
            distance_threshold=distance_threshold,
            return_fields=["id"]
        )
        results = memory_index.query(vector_query)
        if results:
            return True
        return False

    def store_memory(
            self,
            content: str,
            memory_type: MemoryType,
            user_id: str,
            thread_id: str | None = None,
            metadata: str | None = None
    ) -> None:
        memory_index = self._get_or_create_index()
        if metadata is None:
            metadata = "{}"
        memory_exists = self.similar_memory_exists(
            content, memory_type, user_id, thread_id
        )
        if memory_exists:
            return
        embedding = self.vectorizer.embed(content)
        memory_data = {
            "user_id": user_id,
            "content": content,
            "memory_type": memory_type.value,
            "metadata": metadata,
            "created_at": datetime.now().isoformat(),
            "embedding": embedding,
            "memory_id": str(ULID()),
            "thread_id": thread_id,
        }
        try:
            memory_index.load([memory_data])
        except Exception as e:
            logger.exception("Error storing memory: %s", str(e))
            return

    async def retrieve(
            self,
            query: str,
            user_id: str,
            memory_type: MemoryType | list[MemoryType] | None = None,
            thread_id: str | None = None,
            distance_threshold: float = DISTANCE_THRESHOLD,
            limit: int = LIMIT,
    ) -> list[StoredMemory]:
        memory_index = self._get_or_create_index()
        vector_query = VectorRangeQuery(
            vector=self.vectorizer.embed(query),
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
        results = memory_index.query(vector_query)
        memories: list[StoredMemory] = []
        for result in results:
            try:
                memories.append(StoredMemory(**result))
            except Exception as e:
                logger.exception("Error parsing memory: %s", str(e))
        return memories


class AsyncRedisMemoryStorage:
    def __init__(
            self,
            client: AsyncRedis,
            schema: IndexSchema,
            vectorizer: BaseVectorizer
    ) -> None:
        self.client = client
        self.schema = schema
        self.vectorizer = vectorizer

    async def _get_or_create_index(self) -> AsyncSearchIndex:
        try:
            memory_index = AsyncSearchIndex(
                schema=self.schema,
                redis_client=self.client,
                validate_on_load=True
            )
            await memory_index.create(overwrite=False)
        except SchemaValidationError as e:
            logger.exception("Error creating schema: %s", str(e))

    async def similar_memory_exists(
            self,
            content: str,
            memory_type: MemoryType,
            user_id: str,
            thread_id: str | None = None,
            distance_threshold: float = DISTANCE_THRESHOLD,
    ) -> bool:
        memory_index = await self._get_or_create_index()
        filters = (Tag("user_id") == user_id) & (Tag("memory_type") == memory_type)
        if thread_id:
            filters = filters & (Tag("thread_id") == thread_id)
        content_embedding = self.vectorizer.embed(content)
        vector_query = VectorRangeQuery(
            vector=content_embedding,
            num_results=NUM_RESULTS,
            vector_field_name="embedding",
            filter_expression=filters,
            distance_threshold=distance_threshold,
            return_fields=["id"]
        )
        results = await memory_index.query(vector_query)
        if results:
            return True
        return False

    async def store_memory(
            self,
            content: str,
            memory_type: MemoryType,
            user_id: str,
            thread_id: str | None = None,
            metadata: str | None = None
    ) -> None:
        memory_index = await self._get_or_create_index()
        if metadata is None:
            metadata = "{}"
        memory_exists = await self.similar_memory_exists(
            content, memory_type, user_id, thread_id
        )
        if memory_exists:
            return
        embedding = self.vectorizer.embed(content)
        memory_data = {
            "user_id": user_id,
            "content": content,
            "memory_type": memory_type.value,
            "metadata": metadata,
            "created_at": datetime.now().isoformat(),
            "embedding": embedding,
            "memory_id": str(ULID()),
            "thread_id": thread_id,
        }
        try:
            await memory_index.load([memory_data])
        except Exception as e:
            logger.exception("Error storing memory: %s", str(e))
            return

    async def retrieve(
            self,
            query: str,
            user_id: str,
            memory_type: MemoryType | list[MemoryType] | None = None,
            thread_id: str | None = None,
            distance_threshold: float = DISTANCE_THRESHOLD,
            limit: int = LIMIT,
    ) -> list[StoredMemory]:
        memory_index = await self._get_or_create_index()
        vector_query = VectorRangeQuery(
            vector=self.vectorizer.embed(query),
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
        memories: list[StoredMemory] = []
        for result in results:
            try:
                memories.append(StoredMemory(**result))
            except Exception as e:
                logger.exception("Error parsing memory: %s", str(e))
        return memories
