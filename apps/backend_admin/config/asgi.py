"""
ASGI config for config project.
"""

import os
import asyncio
import logging
from django.core.asgi import get_asgi_application
from utils.ping_flyio import ping_flyio

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# ASGI 애플리케이션 초기화
application = get_asgi_application()


# 핑 서비스 시작
async def start_ping_service():
    logger.info("Starting FastAPI ping service...")
    try:
        await ping_flyio()
    except Exception as e:
        logger.error(f"Error in ping service: {e}")


# ASGI 애플리케이션 시작 시 핑 서비스 시작
asyncio.create_task(start_ping_service())
