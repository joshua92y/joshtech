# backend_api/app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import Response
from dotenv import load_dotenv
import os

# ✅ 커스텀 미들웨어 및 유틸
from .utils.scheduler import start as start_scheduler
from .middleware.auth_middleware import AuthMiddleware
from .decorators.auth import auth_required
from .deps.redis_client import redis_client

# ✅ 환경 변수 로드 (.env)
load_dotenv()

# ✅ FastAPI 앱 초기화
app = FastAPI(
    title=os.getenv("API_NAME", "portfolio-api"),
    description="Developer portfolio API server (FastAPI) without Django",
    version="0.1.0",
)

# ✅ 커스텀 인증 미들웨어 적용
app.add_middleware(AuthMiddleware)

# ✅ 전역 OPTIONS 요청 핸들링 (CORS 프리플라이트 대응, Traefik에서 CORS 헤더 처리 전제)
@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    return Response(status_code=204)

# ✅ 라우터 모듈 등록 (대소문자 주의)
from .routers import (
    contactAPI,
    projectAPI,
    resumeAPI,
    frontAPI,
    securityAPI,
    accounts,
    R2_Storage,
)

app.include_router(resumeAPI.router)
app.include_router(projectAPI.router)
app.include_router(contactAPI.router)
app.include_router(frontAPI.router)
app.include_router(securityAPI.router)
app.include_router(accounts.router)
app.include_router(R2_Storage.router)

# ✅ 기본 루트 응답
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI API!"}

# ✅ 헬스 체크 엔드포인트
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

# ✅ FastAPI 애플리케이션 시작 시 실행되는 이벤트
@app.on_event("startup")
async def startup_event():
    # Redis 연결 확인
    try:
        pong = await redis_client.ping()
        if pong:
            print("✅ Redis 연결 성공")
    except Exception as e:
        print(f"❌ Redis 연결 실패: {e}")

    # 주기 작업 스케줄러 시작
    start_scheduler()

# ✅ 인증 테스트용 라우트 (유저 정보가 있으면 인사, 없으면 게스트 인사)
@app.get("/hello")
async def hello(request: Request):
    user = request.state.user  # 인증되지 않았을 경우 None
    return {"message": f"Hello {user['username']}" if user else "Hello Guest"}

# ✅ 보호된 라우트 (인증 필요)
@app.get("/secure-data")
@auth_required()
async def get_secure(request: Request):
    return {"secure": True, "user": request.state.user}
