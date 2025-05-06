#backend_api\app\routers\resumeAPI.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from Resume import Resume  # 조회용 (기존 유지)
import httpx

router = APIRouter()

# ✅ 이력서 제출용 요청 스키마
class ResumeCreateRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    summary: str

# ✅ Django API 호출 함수
DJANGO_API_URL = "https://your-django-app.onrender.com/api/resume/"  # 실제 Render 주소로 교체

async def send_resume_to_django(data: dict) -> dict:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(DJANGO_API_URL, json=data)
            if response.status_code == 201:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.json())
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Django 서버와 통신 실패: {e}")


# ✅ 정적 이력서 조회 (GET)
@router.get(
    "/resume",
    response_model=Resume,
    summary="개발자 이력서 정보 조회",
    description="이 API는 정적인 샘플 개발자 이력서 정보를 반환합니다.",
    response_description="이력서 정보 반환 성공",
)
def get_resume():
    return Resume(
        name="홍길동",
        email="hong@example.com",
        phone="010-1234-5678",
        summary="FastAPI + Django 기반 백엔드 개발자",
    )


# ✅ 동적 이력서 제출 (POST)
@router.post(
    "/resume",
    summary="이력서 제출",
    description="사용자가 입력한 이력서 정보를 Render에 배포된 Django API로 전달하여 저장합니다.",
    response_description="이력서 제출 성공"
)
async def submit_resume(payload: ResumeCreateRequest):
    return await send_resume_to_django(payload.dict())
