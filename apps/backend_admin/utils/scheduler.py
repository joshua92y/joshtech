# apps\backend_admin\utils\scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import asyncio

from utils.ping_flyio import ping_flyio
from utils.R2_Storage import clean_soft_deleted_files

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def start():
    scheduler.add_job(
        func=lambda: asyncio.run(ping_flyio()),
        trigger="interval",
        minutes=5,
        id="ping_flyio",
        replace_existing=True,
    )

    scheduler.add_job(
        func=lambda: asyncio.run(clean_soft_deleted_files()),
        trigger="interval",
        minutes=10,
        id="r2_cleanup",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("✅ APScheduler started with ping and R2 cleanup tasks.")
