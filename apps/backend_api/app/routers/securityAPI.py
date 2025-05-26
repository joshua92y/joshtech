# backend_api/app/routers/securityAPI.py
import os
from fastapi import APIRouter, Request, Cookie, status, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/security", tags=["Security"])


@router.get("/check-auth")
def check_auth(authToken: str = Cookie(default=None)):
    if authToken == "authenticated":
        return JSONResponse(content={"authenticated": True}, status_code=200)
    return JSONResponse(content={"authenticated": False}, status_code=401)


@router.post("/authenticate")
async def authenticate(request: Request):
    body = await request.json()
    password = body.get("password")
    correct_password = os.getenv("PAGE_ACCESS_PASSWORD", "2025")

    if not correct_password:
        raise HTTPException(status_code=500, detail="Server misconfigured")

    if password == correct_password:
        response = JSONResponse(
            content={"success": True}, status_code=status.HTTP_200_OK
        )
        response.set_cookie(
            key="authToken",
            value="authenticated",
            httponly=True,
            # secure가 True일 경우 https만 쿠키 허용
            secure=True,
            max_age=60 * 60,
            samesite="none",
            path="/",
            domain="joshuatech.dev",
        )
        return response
    else:
        return JSONResponse(
            content={"message": "Incorrect password"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
