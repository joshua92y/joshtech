# backend-api/app/main.py
import django
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# 경로 설정
BASE_DIR = Path(__file__).resolve().parents[3]  # joshtech
sys.path.append(str(BASE_DIR / "apps"))  # backend_admin 찾기 위함
sys.path.append(str(BASE_DIR / "apps" / "backend_admin"))  # config 찾기 위함
sys.path.append(str(BASE_DIR / "packages" / "shared_schemas"))

# print("[DEBUG] sys.path 목록:")
# for p in sys.path:
#    print("  -", p)
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

# ✅ 라우터 등록
from .routers import contactAPI, projectAPI, resumeAPI

app.include_router(resumeAPI.router)
app.include_router(projectAPI.router)
app.include_router(contactAPI.router)


# 기본 루트
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI API!"}
