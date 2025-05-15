# apps\backend_admin\config\asgi.py
"""
ASGI config for config project.
"""

import os
import asyncio
import logging
from django.core.asgi import get_asgi_application
from utils.scheduler import start as start_scheduler

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# ASGI 애플리케이션 초기화
application = get_asgi_application()

start_scheduler()
