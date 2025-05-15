from fastapi import Depends, HTTPException, Request
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

DJANGO_VERIFY_URL = os.getenv(
    "DJANGO_VERIFY_URL", "https://admin.joshuatech.dev/api/accounts/token-verify/"
)


async def get_current_user(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = auth.removeprefix("Bearer ").strip()

    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(
                DJANGO_VERIFY_URL,
                headers={"Authorization": f"Bearer {token}"},
                timeout=5,
            )
            res.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception:
            raise HTTPException(status_code=500, detail="Token verification failed")

    return res.json()  # → { id, username, uuid }
