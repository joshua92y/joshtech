# ✅ apps/worker/r2_worker.py

import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

import httpx
from dotenv import load_dotenv

# ✅ 경로 추가
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../packages/shared_queue")
    )
)

from redis_queue import delete_queue

import boto3
from botocore.client import Config

load_dotenv()

R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_BUCKET = os.getenv("R2_BUCKET")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
DJANGO_API = os.getenv("DJANGO_API_URL")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("r2_worker")

s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="auto",
)


# ✅ R2 삭제 함수
def delete_r2_object(key: str) -> bool:
    try:
        s3.delete_object(Bucket=R2_BUCKET, Key=key)
        logger.info(f"✅ R2 삭제 완료: {key}")
        return True
    except Exception as e:
        logger.error(f"❌ R2 삭제 실패 ({key}): {e}")
        return False


# ✅ soft-delete 상태 확인
async def is_soft_deleted(client: httpx.AsyncClient, file_id: int) -> bool:
    try:
        res = await client.get(f"{DJANGO_API.rstrip('/')}/api/r2/files/{file_id}/")
        res.raise_for_status()
        file_info = res.json()
        return file_info.get("is_deleted", False) is True
    except Exception as e:
        logger.warning(f"⚠️ Django 상태 조회 실패(id={file_id}): {e}")
        return False


# ✅ 메인 워커 루프
async def worker_loop():
    logger.info("🚀 R2 삭제 워커 시작")
    async with httpx.AsyncClient() as client:
        while True:
            try:
                task: Dict[str, Any] = await delete_queue.dequeue()
                key = task.get("key")
                pk = task.get("id")
                enqueued_at = task.get("enqueued_at")

                # 유효성 검사
                if not key or not pk or not enqueued_at:
                    logger.warning(f"⚠️ 잘못된 task: {task}")
                    continue

                # 대기 시간 검사
                enqueue_time = datetime.fromisoformat(enqueued_at)
                if datetime.utcnow() - enqueue_time < timedelta(minutes=10):
                    logger.info(f"⏳ 대기 시간 부족 (id={pk}), 건너뜀")
                    await asyncio.sleep(1)
                    continue

                # soft-delete 상태 확인
                if not await is_soft_deleted(client, pk):
                    logger.info(f"❌ 삭제 취소됨 (id={pk}): soft-delete 상태 아님")
                    continue

                # 실제 R2 삭제
                if delete_r2_object(key):
                    payload = [
                        {
                            "id": pk,
                            "is_purged": True,
                            "purged_at": datetime.utcnow().isoformat(),
                        }
                    ]
                    try:
                        res = await client.post(
                            f"{DJANGO_API.rstrip('/')}/api/r2/files/deletion-complete/",
                            json=payload,
                        )
                        res.raise_for_status()
                        logger.info(f"🧹 Django에 삭제 결과 보고 완료: {pk}")
                    except Exception as e:
                        logger.error(f"❌ Django 보고 실패 (id={pk}): {e}")

            except Exception as e:
                logger.exception("❌ 워커 처리 중 예외 발생")
                await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(worker_loop())
