from datetime import timedelta

from langchain_core.messages import BaseMessage
from redis.asyncio import Redis as AsyncRedis

DEFAULT_LAST = 10
DEFAULT_TTL = timedelta(hours=1)


class RedisChatHistory:
    def __init__(self, redis: AsyncRedis, ttl: timedelta = DEFAULT_TTL) -> None:
        self.redis = redis
        self.ttl = ttl

    async def add_messages(
            self, chat_id: str, messages: list[BaseMessage]
    ) -> None:
        values = [message.model_dump_json() for message in messages]
        await self.redis.lpush(chat_id, *values)
        await self.redis.expire(chat_id, self.ttl)

    async def get_messages(
            self, chat_id: str, last: int = DEFAULT_LAST
    ) -> list[BaseMessage]:
        values = await self.redis.lrange(chat_id, 0, -1)
        return [BaseMessage.model_validate_json(value) for value in values[:last]]
