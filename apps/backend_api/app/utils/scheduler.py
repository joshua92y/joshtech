# app/utils/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from .ping_flyio import ping_render
from pathlib import Path
import logging
import asyncio
import time
import os
from html2image import Html2Image
import boto3
from botocore.client import Config
import httpx
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


# 환경 변수
R2_ENDPOINT = os.getenv(
    "R2_ENDPOINT",
    "https://91738ffff95834c5972f1a92aac416a6.r2.cloudflarestorage.com/joshtech",
)
R2_BUCKET = os.getenv("R2_BUCKET", "joshtech")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY", "91738ffff95834c5972f1a92aac416a6")
R2_SECRET_KEY = os.getenv(
    "R2_SECRET_KEY", "8d3446847d630f900e2521d0efc35a5cd5f92e50cd620987cdbd85f33978f070"
)
DJANGO_API = os.getenv(
    "DJANGO_API_URL", "https://your-django-api.com/api/files/"
)  # Django 백엔드에서 운영 중인 파일 메타데이터 API의 Base URL입니다.

# R2 클라이언트
s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="auto",
)


async def clean_soft_deleted_files():
    async with httpx.AsyncClient() as client:
        try:
            # ✅ 1. Django에서 삭제 대기 파일 가져오기
            res = await client.get(DJANGO_API + "deletion-pending/")
            res.raise_for_status()
            to_delete = res.json()
        except Exception as e:
            logger.exception(f"❌ 삭제 목록 조회 실패: {e}")
            return

        deleted_ids = []

        # ✅ 2. R2에서 실제 삭제 수행
        for item in to_delete:
            key = item["key"]
            pk = item["id"]
            try:
                s3.delete_object(Bucket=R2_BUCKET, Key=key)
                deleted_ids.append(pk)
                logger.info(f"✅ 삭제 완료: {key}")
            except Exception as e:
                logger.exception(f"❌ R2 삭제 실패: {key} - {e}")

        # ✅ 3. Django에 삭제 완료 보고
        if deleted_ids:
            try:
                res = await client.post(
                    DJANGO_API + "deletion-complete/", json={"ids": deleted_ids}
                )
                res.raise_for_status()
                logger.info(f"🧹 Django에 삭제 완료 보고: {len(deleted_ids)}건")
            except Exception as e:
                logger.exception(f"❌ Django 삭제 보고 실패: {e}")


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

    scheduler.add_job(
        func=lambda: asyncio.run(clean_soft_deleted_files()),
        trigger="interval",
        minutes=10,
        id="r2_cleanup",
    )
    scheduler.start()
    logger.info("✅ APScheduler started for all jobs.")
