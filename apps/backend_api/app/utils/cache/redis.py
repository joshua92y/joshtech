# app/utils/cache/redis.py
from redis.asyncio import Redis
import httpx
import json
from app.config.settings import settings

redis = Redis()


async def get_user_info(token: str):
    cache_key = f"{settings.env}:auth:user:jwt:{token}"

    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)

    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{settings.auth_verify_url}", headers={"Authorization": token}
        )
        if res.status_code == 200:
            user_info = res.json()
            ttl = 60 if user_info["role"]["name"] == "admin" else 300
            await redis.set(cache_key, json.dumps(user_info), ex=ttl)
            return user_info
    return None
