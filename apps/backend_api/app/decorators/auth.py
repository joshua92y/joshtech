# app/decorators/auth.py
import asyncio
from fastapi import Request, HTTPException
from functools import wraps


def _extract_request(args, kwargs):
    return kwargs.get("request") or next(
        (a for a in args if isinstance(a, Request)), None
    )


def auth_required():
    def decorator(func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                request = _extract_request(args, kwargs)
                if not request or not request.state.user:
                    raise HTTPException(401, detail="인증이 필요합니다.")
                return await func(*args, **kwargs)

            return async_wrapper
        else:

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                request = _extract_request(args, kwargs)
                if not request or not request.state.user:
                    raise HTTPException(401, detail="인증이 필요합니다.")
                return func(*args, **kwargs)

            return sync_wrapper

    return decorator


def role_required(required_role: str):
    def decorator(func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                request = _extract_request(args, kwargs)
                user = getattr(request.state, "user", None)
                if not user or user["role"]["name"] != required_role:
                    raise HTTPException(403, detail="접근 권한 없음")
                return await func(*args, **kwargs)

            return async_wrapper
        else:

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                request = _extract_request(args, kwargs)
                user = getattr(request.state, "user", None)
                if not user or user["role"]["name"] != required_role:
                    raise HTTPException(403, detail="접근 권한 없음")
                return func(*args, **kwargs)

            return sync_wrapper

    return decorator
