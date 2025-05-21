# ✅ packages/shared_queue/redis_queue.py
from abc import ABC, abstractmethod
import json
import os
from redis.asyncio import Redis


# ✅ 추상 큐 인터페이스
class BaseQueue(ABC):
    @abstractmethod
    async def enqueue(self, data: dict): ...

    @abstractmethod
    async def dequeue(self) -> dict: ...


# ✅ Redis 구현체
class RedisQueue(BaseQueue):
    def __init__(self, redis_url: str = None, queue_name: str = "delete_queue"):
        redis_url = redis_url or os.getenv("DRAGONFLY_URL", "redis://localhost:6379")
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.queue_name = queue_name

    async def enqueue(self, data: dict):
        await self.redis.lpush(self.queue_name, json.dumps(data))

    async def dequeue(self) -> dict:
        _, raw = await self.redis.brpop(self.queue_name)
        return json.loads(raw)


# ✅ 싱글톤 인스턴스 (delete 전용)
delete_queue = RedisQueue()
