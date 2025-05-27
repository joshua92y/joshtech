# app/middleware/auth_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.utils.cache.redis import get_user_info

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # ✅ CORS Preflight OPTIONS 요청도 CORSMiddleware까지 흐르게 함
        if request.method == "OPTIONS":
            return await call_next(request)

        token = request.headers.get("Authorization")
        request.state.user = None

        if token and token.startswith("Bearer "):
            user_info = await get_user_info(token)
            if user_info:
                request.state.user = user_info

        return await call_next(request)
