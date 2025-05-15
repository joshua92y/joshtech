# app/decorators/auth.py
from fastapi import Request, HTTPException
from functools import wraps


def auth_required():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request") or next(
                (a for a in args if isinstance(a, Request)), None
            )
            if not request or not request.state.user:
                raise HTTPException(401, detail="인증이 필요합니다.")
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def role_required(required_role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request") or next(
                (a for a in args if isinstance(a, Request)), None
            )
            user = getattr(request.state, "user", None)
            if not user or user["role"]["name"] != required_role:
                raise HTTPException(403, detail="접근 권한 없음")
            return await func(*args, **kwargs)

        return wrapper

    return decorator
