# app/deps/redis_client.py
import redis.asyncio as redis
from app.config.settings import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=True,
)
