# backend-api/app/routers/project.py
from fastapi import APIRouter
from Project import Project

router = APIRouter()


@router.get("/projects", response_model=list[Project])
def get_projects():
    return [
        Project(
            title="AI Tone Converter",
            description="말투를 AI로 분석하고 변환해주는 웹 앱",
            link="https://github.com/yourname/tone-c",
        ),
        Project(
            title="포트폴리오 사이트",
            description="개발자 이력과 프로젝트를 정리한 개인 웹사이트",
        ),
    ]
