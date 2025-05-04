# backend-api/app/main.py
import django
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# 📦 BASE_DIR = 컨테이너 내에서 FastAPI 앱 루트 위치
BASE_DIR = Path(__file__).resolve().parent

# ✅ Django 경로 세팅: /app/backend_admin
sys.path.append(str(BASE_DIR / "backend_admin"))  # /app/backend_admin/config/settings.py 기준

# ✅ 공통 스키마(shared_schemas) 위치 세팅: /shared_schemas
sys.path.append("/shared_schemas")

# Django 설정 연결
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_admin.config.settings")
django.setup()

# .env 로드
load_dotenv()

# FastAPI 앱 초기화
app = FastAPI(
    title=os.getenv("API_NAME", "portfolio-api"),
    description="Developer portfolio API server (FastAPI)",
    version="0.1.0",
)

# 라우터 등록
from .routers import contactAPI, projectAPI, resumeAPI

app.include_router(resumeAPI.router)
app.include_router(projectAPI.router)
app.include_router(contactAPI.router)

# 기본 라우트
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI API!"}
