# backend_api\app\main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from .utils.scheduler import start as start_scheduler

# .env 로드
load_dotenv()

# FastAPI 앱 초기화
app = FastAPI(
    title=os.getenv("API_NAME", "portfolio-api"),
    description="Developer portfolio API server (FastAPI) without Django",
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


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    start_scheduler()
