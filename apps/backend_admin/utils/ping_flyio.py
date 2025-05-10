# apps/backend_admin/utils/ping_flyio.py

import asyncio
import httpx
import os
from django.conf import settings


async def ping_flyio():
    url = os.getenv("FASTAPI_URL", "https://joshtech-api.fly.dev/healthz")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            print(f"[Render → Fly] Ping OK: {response.status_code}")
    except Exception as e:
        print(f"[Render → Fly] Ping Error: {e}")
