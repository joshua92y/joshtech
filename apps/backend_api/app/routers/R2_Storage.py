# src/app/routers/R2_Storage.py
from fastapi import APIRouter, HTTPException
import boto3, os
from botocore.client import Config
from uuid import uuid4
from datetime import datetime
import httpx

from FileMeta import FileMeta  # ✅ 외부 모델 import

router = APIRouter()

# ✅ 환경 변수
R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_BUCKET = os.getenv("R2_BUCKET")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
DJANGO_API_URL = os.getenv("DJANGO_API_URL", "https://your-django-api.com/api/files/")

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
    filename: str  # 예: myfile.pdf
    content_type: str  # 예: application/pdf


@router.post("/upload-url")
def get_upload_url(data: UploadRequest):
    ext = data.filename.split(".")[-1]
    key = f"uploads/{uuid4().hex}.{ext}"

    try:
        presigned_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": R2_BUCKET,
                "Key": key,
                "ContentType": data.content_type,
            },
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
    # ✅ uploaded_at 값 강제 입력 (UTC 현재 시각)
    file_meta = data.copy(update={"uploaded_at": datetime.utcnow()})

    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(DJANGO_API_URL, json=file_meta.dict(), timeout=10)
            res.raise_for_status()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Django 저장 실패: {e}")

    return {"status": "ok", "saved": file_meta.dict()}
