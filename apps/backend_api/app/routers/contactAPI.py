from fastapi import APIRouter, Body, HTTPException
from Contactmessage import ContactMessage
import httpx
import os

router = APIRouter()
DJANGO_CONTACT_API_URL = "https://your-django-app.onrender.com/api/resume/"
# ✅ Django API 엔드포인트 URL을 환경 변수에서 읽어옵니다.
# 환경 변수 이름은 예시입니다. 실제 설정할 이름과 일치시켜야 합니다.
DJANGO_CONTACT_API_URL = os.getenv("DJANGO_CONTACT_API_URL")


@router.post(
    "/contact",
    response_model=ContactMessage,
    summary="문의 메시지 제출",
    description="사용자로부터 문의 메시지를 수신합니다.",
    response_description="제출된 메시지 반환",
)
async def submit_contact(msg: ContactMessage):  # 비동기 함수로 유지
    if not DJANGO_CONTACT_API_URL:
        # ✅ 환경 변수가 설정되지 않았으면 에러 발생
        raise HTTPException(
            status_code=500, detail="Django contact API URL not configured"
        )

    # ✅ Django API로 데이터 전송
    async with httpx.AsyncClient() as client:
        try:
            # ✅ Django API 엔드포인트 URL로 POST 요청 보냄
            # msg.model_dump_json() 또는 msg.dict() 사용 (FastAPI/Pydantic 버전에 따라 다름)
            response = await client.post(
                DJANGO_CONTACT_API_URL,
                json=msg.model_dump(mode="json"),  # Pydantic V2+
                # json=msg.dict() # Pydantic V1
            )
            response.raise_for_status()  # 2xx 응답이 아니면 HTTPStatusError 발생

        except httpx.HTTPStatusError as e:
            # ✅ Django API에서 오류 응답을 받았을 때 처리
            print(
                f"Error from Django API: {e.response.status_code} - {e.response.text}"
            )
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error submitting contact message to Django API: {e.response.text}",
            )
        except httpx.RequestError as e:
            # ✅ 네트워크 오류 등 요청 자체의 오류 발생 시 처리
            print(f"Request error to Django API: {e}")
            raise HTTPException(
                status_code=503, detail=f"Could not connect to Django contact API: {e}"
            )
        except Exception as e:
            # ✅ 기타 예외 처리
            print(f"An unexpected error occurred while calling Django API: {e}")
            raise HTTPException(
                status_code=500, detail=f"An unexpected error occurred: {e}"
            )

    # ✅ Django ORM 호출 대신 API 호출 성공 시 메시지 반환
    # Django API가 성공 응답 (예: 200 OK, 201 Created)을 보냈다면 이 부분이 실행됩니다.
    return msg
