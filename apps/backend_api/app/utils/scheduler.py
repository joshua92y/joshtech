from apscheduler.schedulers.background import BackgroundScheduler
from .ping_flyio import ping_render
import logging
import asyncio

logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler()

    # 주기적 작업 등록: 5분마다
    scheduler.add_job(
        func=lambda: asyncio.run(ping_render()),
        trigger='interval',
        minutes=5,
        id='ping_render',
        replace_existing=True,
    )

    scheduler.start()
    logger.info("✅ APScheduler started for ping_render.")
