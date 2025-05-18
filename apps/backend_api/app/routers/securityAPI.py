# backend_api/app/routers/securityAPI.py
import os
from fastapi import APIRouter, Request, Cookie, status, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/check-auth")
def check_auth(authToken: str = Cookie(default=None)):
    if authToken == "authenticated":
        return JSONResponse(content={"authenticated": True}, status_code=200)
    return JSONResponse(content={"authenticated": False}, status_code=401)


@router.post("/check-auth")
async def check_auth(request: Request):
    body = await request.json()
    password = body.get("password")
    correct_password = os.getenv("PAGE_ACCESS_PASSWORD")

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
            secure=os.getenv("ENV") == "production",  # 또는 직접 NODE_ENV로
            max_age=60 * 60,
            samesite="strict",
            path="/",
        )
        return response
    else:
        return JSONResponse(
            content={"message": "Incorrect password"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
