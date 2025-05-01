# backend-api/app/routers/resume.py

from fastapi import APIRouter
from Resume import Resume

router = APIRouter()


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
