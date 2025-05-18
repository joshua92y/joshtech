# app/utils/cache/redis.py

from aiocache import caches, cached
import httpx
import json
from app.config.settings import settings

# 기본 캐시 설정 (Redis 사용)
caches.set_config(
    {
        "default": {
            "cache": "aiocache.RedisCache",
            "endpoint": settings.redis_host,  # 예: "localhost"
            "port": settings.redis_port,  # 예: 6379
            "timeout": 1,
            "serializer": {"class": "aiocache.serializers.JsonSerializer"},
        }
    }
)


async def get_user_info(token: str):
    cache_key = f"{settings.env}:auth:user:jwt:{token}"
    cache = caches.get("default")

    cached = await cache.get(cache_key)
    if cached:
        return cached  # 이미 JSON 역직렬화된 객체

    async with httpx.AsyncClient() as client:
        res = await client.get(
            settings.auth_verify_url, headers={"Authorization": token}
        )
        if res.status_code == 200:
            user_info = res.json()
            ttl = 60 if user_info["role"]["name"] == "admin" else 300
            await cache.set(cache_key, user_info, ttl=ttl)
            return user_info

    return None
