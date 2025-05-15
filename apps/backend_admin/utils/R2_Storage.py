# apps\backend_admin\utils\R2_Storage.py
import os
import boto3
from botocore.client import Config
import httpx
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
logger = logging.getLogger(__name__)

# ✅ 환경 변수 (기본값 제거 + 예외 처리 가능)
R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_BUCKET = os.getenv("R2_BUCKET")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
DJANGO_API = os.getenv("DJANGO_API_URL")

if not all([R2_ENDPOINT, R2_BUCKET, R2_ACCESS_KEY, R2_SECRET_KEY, DJANGO_API]):
    raise EnvironmentError("❌ R2 또는 Django API 설정이 누락되었습니다.")

# ✅ R2 클라이언트 설정
s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="auto",
)


# ✅ 파일 삭제 함수
def delete_r2_object(key: str) -> bool:
    try:
        s3.delete_object(Bucket=R2_BUCKET, Key=key)
        logger.info(f"✅ R2 삭제 완료: {key}")
        return True
    except Exception as e:
        logger.exception(f"❌ R2 삭제 실패 ({key}): {e}")
        return False


# ✅ 메인 루틴
async def clean_soft_deleted_files():
    deleted_payload = []

    async with httpx.AsyncClient() as client:
        try:
            # 1. 삭제 대상 조회
            response = await client.get(f"{DJANGO_API.rstrip('/')}/deletion-pending/")
            response.raise_for_status()
            to_delete: List[Dict[str, Any]] = response.json()
        except Exception as e:
            logger.exception(f"❌ 삭제 대상 조회 실패: {e}")
            return

        # 2. R2 삭제 루프
        for item in to_delete:
            key = item.get("key")
            pk = item.get("id")
            if key and pk and delete_r2_object(key):
                deleted_payload.append(
                    {
                        "id": pk,
                        "is_purged": True,
                        "purged_at": datetime.utcnow().isoformat(),
                    }
                )

        # 3. 삭제 완료 보고 (is_purged 포함)
        if deleted_payload:
            try:
                res = await client.post(
                    f"{DJANGO_API.rstrip('/')}/deletion-complete/",
                    json=deleted_payload,
                )
                res.raise_for_status()
                logger.info(f"🧹 Django에 삭제 완료 보고: {len(deleted_payload)}건")
            except Exception as e:
                logger.exception(f"❌ Django 삭제 완료 보고 실패: {e}")
