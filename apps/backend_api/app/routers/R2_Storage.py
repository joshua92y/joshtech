# src/app/routers/R2_Storage.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import boto3, os
from botocore.client import Config
from uuid import uuid4
from datetime import datetime
import httpx
from redis_queue import delete_queue  # ✅ 큐 import

from FileMeta import FileMeta  # ✅ 외부 모델 import

router = APIRouter(prefix="/r2", tags=["R2 Storage"])

# ✅ 환경 변수
R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_BUCKET = os.getenv("R2_BUCKET")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
DJANGO_API_URL = os.getenv("DJANGO_API_URL")

# ✅ R2 클라이언트 초기화
s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
    region_name="auto",
    config=Config(signature_version="s3v4"),
)


class UploadRequest(BaseModel):
    filename: str
    content_type: str


@router.post("/upload-url")
def get_upload_url(data: UploadRequest):
    ext = data.filename.split(".")[-1]
    key = f"uploads/{uuid4().hex}.{ext}"

    try:
        presigned_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": R2_BUCKET, "Key": key, "ContentType": data.content_type},
            ExpiresIn=600,
        )

        return {
            "upload_url": presigned_url,
            "key": key,
            "expires_in": 600,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-callback")
async def upload_callback(data: FileMeta):
    file_meta = data.copy(update={"uploaded_at": datetime.utcnow()})

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(
                f"{DJANGO_API_URL.rstrip('/')}/api/r2/files/",
                json=file_meta.dict(),
                timeout=10,
            )
            res.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Django 저장 실패: {e}")

    return {"status": "ok", "saved": file_meta.dict()}


# ✅ 삭제 요청 처리 + 큐 등록
class DeleteRequest(BaseModel):
    id: int
    key: str  # 삭제 키는 프론트 or DB에서 미리 조회 필요


@router.delete("/delete")
async def delete_file(data: DeleteRequest):
    async with httpx.AsyncClient() as client:
        try:
            # 1. Django에 소프트 삭제 요청
            res = await client.delete(
                f"{DJANGO_API_URL.rstrip('/')}/api/r2/files/{data.id}/",
                params={"from": "fastapi", "by": "admin"},
                timeout=10,
            )
            res.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Django 삭제 실패: {e}")

        # 2. Redis 큐에 등록
        try:
            await delete_queue.enqueue(
                {
                    "id": data.id,
                    "key": data.key,
                    "enqueued_at": datetime.utcnow().isoformat(),
                }
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"큐 등록 실패: {e}")
