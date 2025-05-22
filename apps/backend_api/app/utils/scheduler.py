# app/utils/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from .ping_flyio import ping_render
from pathlib import Path
import logging
import asyncio
import time
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

TMP_DIR = Path("tmp")
TTL_SECONDS = int(os.getenv("TMP_TTL_SECONDS", "300"))  # 5분
CLEANUP_INTERVAL_MIN = int(os.getenv("CLEANUP_INTERVAL_MIN", "5"))


def clean_tmp_folder():
    now = time.time()
    deleted = 0

    for file in TMP_DIR.glob("*"):
        if file.is_file() and now - file.stat().st_mtime > TTL_SECONDS:
            try:
                file.unlink()
                deleted += 1
            except Exception:
                logger.exception(f"❌ {file} 삭제 실패")
    if deleted:
        logger.info(f"🧹 {deleted}개 임시 파일 삭제 완료")


def start():
    scheduler.add_job(
        func=lambda: asyncio.run(ping_render()),
        trigger="interval",
        minutes=5,
        id="ping_render",
        replace_existing=True,
    )
    scheduler.add_job(
        func=clean_tmp_folder,
        trigger="interval",
        minutes=CLEANUP_INTERVAL_MIN,
        id="tmp_cleanup",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("✅ APScheduler started for all jobs.")
