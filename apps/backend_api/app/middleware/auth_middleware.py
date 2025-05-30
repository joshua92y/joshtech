# app/middleware/auth_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.utils.cache.redis import get_user_info

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        token = request.headers.get("Authorization")
        request.state.user = None

        if token and token.startswith("Bearer "):
            user_info = await get_user_info(token)
            if user_info:
                request.state.user = user_info

        return await call_next(request)