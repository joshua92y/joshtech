# backend_api\app\main.py
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
from .utils.scheduler import start as start_scheduler
from .middleware.auth_middleware import AuthMiddleware
from .decorators.auth import auth_required

# .env 로드
load_dotenv()

# FastAPI 앱 초기화
app = FastAPI(
    title=os.getenv("API_NAME", "portfolio-api"),
    description="Developer portfolio API server (FastAPI) without Django",
    version="0.1.0",
)
app.add_middleware(AuthMiddleware)

# ✅ 라우터 등록(대소문자 주의)
from .routers import contactAPI, projectAPI, resumeAPI, frontAPI, securityAPI, accounts

app.include_router(resumeAPI.router)
app.include_router(projectAPI.router)
app.include_router(contactAPI.router)
app.include_router(frontAPI.router)
app.include_router(securityAPI.router)
app.include_router(accounts.router)


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


# ✅ 테스트용 라우터
@app.get("/hello")
async def hello(request: Request):
    user = request.state.user  # None일 수도 있음
    return {"message": f"Hello {user['username']}" if user else "Hello Guest"}


@app.get("/secure-data")
@auth_required()
async def get_secure(request: Request):
    return {"secure": True, "user": request.state.user}
