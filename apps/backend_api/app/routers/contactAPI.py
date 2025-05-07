# backend_api/app/routers/contactAPI.py

from fastapi import APIRouter, HTTPException
import os
from shared_schemas.Contactmessage import ContactMessage
import httpx
from dotenv import load_dotenv
load_dotenv()
router = APIRouter(prefix="/contact", tags=["Contact"])
DJANGO_API_BASE = os.getenv("DJANGO_API_BASE")
DJANGO_API_BASE_CONTACT = f"{DJANGO_API_BASE}/api/contact"

@router.post("/send")
async def send_contact_message(message: ContactMessage):
    # 1. 유효성 검증 요청
    try:
        async with httpx.AsyncClient() as client:
            validate_response = await client.post(f"{DJANGO_API_BASE_CONTACT}/validate/", json=message.dict())
        validate_response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation failed: {str(e)}")

    # 2. SMTP 전송 (예시 placeholder)
    try:
        # 여기에 SMTP 코드 삽입
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SMTP failed: {str(e)}")

    # 3. DB 저장 요청
    try:
        async with httpx.AsyncClient() as client:
            save_response = await client.post(f"{DJANGO_API_BASE_CONTACT}/save/", json=message.dict())
        save_response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Saving failed: {str(e)}")

    return {"detail": "Contact message sent and saved successfully."}
