# backend_api/app/routers/contactAPI.py

from fastapi import APIRouter, HTTPException
import os
from Contactmessage import ContactMessage
import httpx
from dotenv import load_dotenv
from app.utils.utils_postmark import (
    send_email_via_postmark,
)  # 🔁 Postmark 전송 유틸 함수 불러오기
from datetime import datetime

load_dotenv()
router = APIRouter(prefix="/contact", tags=["Contact"])

DJANGO_API_BASE = os.getenv("DJANGO_API_URL")
DJANGO_API_BASE_CONTACT = f"{DJANGO_API_BASE}/api/contact"


@router.post("/send")
async def send_contact_message(message: ContactMessage):
    # 1. 유효성 검증 요청
    try:
        async with httpx.AsyncClient() as client:
            validate_response = await client.post(
                f"{DJANGO_API_BASE_CONTACT}/validate/", json=message.dict()
            )
        validate_response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation failed: {str(e)}")

    # 2. SMTP 전송
    try:
        send_email_via_postmark(message)
        # 전송 성공 시 sent=True, sent_at=현재시간, failure_reason=None
        message.sent = True
        message.sent_at = datetime.now()
        message.failure_reason = None
    except Exception as e:
        # 전송 실패 시 sent=False, sent_at=None, failure_reason=에러메시지
        message.sent = False
        message.sent_at = None
        message.failure_reason = str(e)
        # 실패해도 계속 진행 (HTTPException 제거)

    # 3. DB 저장 요청
    try:
        # datetime 객체를 ISO 형식 문자열로 변환
        message_dict = message.dict()
        if message_dict.get("sent_at"):
            message_dict["sent_at"] = message_dict["sent_at"].isoformat()

        async with httpx.AsyncClient() as client:
            save_response = await client.post(
                f"{DJANGO_API_BASE_CONTACT}/save/", json=message_dict
            )
        save_response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Saving failed: {str(e)}")

    # 4. 응답 메시지 결정
    if message.sent:
        return {"detail": "Contact message sent and saved successfully."}
    else:
        return {
            "detail": "Contact message saved but failed to send.",
            "error": message.failure_reason,
        }
