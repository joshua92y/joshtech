#portfolio\apps\backend-api\app\main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# shared-schemas 경로를 PYTHONPATH에 추가 (가장 먼저!)
BASE_DIR = Path(__file__).resolve().parents[3]  # portfolio/까지 이동
SCHEMA_PATH = BASE_DIR / "packages" / "shared-schemas"
sys.path.append(str(SCHEMA_PATH))
print(f"[DEBUG] shared-schemas 경로 추가됨: {SCHEMA_PATH}")

# 이후에 shared-schemas 모듈 import
from projects import ProjectSchema
from contact import ContactMessageSchema

# .env 파일 로드
load_dotenv()

# FastAPI 앱 초기화
app = FastAPI(
    title=os.getenv("API_NAME", "portfolio-api"),
    description="Developer portfolio API server (FastAPI)",
    version="0.1.0",
)

# 기본 루트
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI API!"}

# 예시 resume 스키마 사용
try:
    from resume import ResumeSchema

    @app.get("/resume", response_model=ResumeSchema)
    def get_resume():
        return ResumeSchema(
            name="홍길동",
            email="hong@example.com",
            phone="010-1234-5678",
            summary="FastAPI + Django 기반 백엔드 개발자"
        )
except ImportError:
    pass  # shared-schemas가 아직 없을 경우를 대비

@app.get("/projects", response_model=list[ProjectSchema])
def get_projects():
    return [
        ProjectSchema(
            title="AI Tone Converter",
            description="말투를 AI로 분석하고 변환해주는 웹 앱",
            link="https://github.com/yourname/tone-c"
        ),
        ProjectSchema(
            title="포트폴리오 사이트",
            description="개발자 이력과 프로젝트를 정리한 개인 웹사이트"
        ),
    ]


@app.post("/contact", response_model=ContactMessageSchema)
def submit_contact(msg: ContactMessageSchema):
    return msg  # 일단은 받은 메시지를 그대로 반환 (저장은 추후 DB 연동 시)