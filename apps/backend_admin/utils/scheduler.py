from apscheduler.schedulers.background import BackgroundScheduler
from utils.ping_flyio import ping_flyio
import logging
import asyncio

logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler()

    # 주기적 작업 등록: 5분마다
    scheduler.add_job(
        func=lambda: asyncio.run(ping_flyio()),
        trigger='interval',
        minutes=5,
        id='ping_flyio',
        replace_existing=True,
    )

    scheduler.start()
    logger.info("✅ APScheduler started for ping_flyio.")
