from fastapi import APIRouter, Depends, Request
from app.deps.auth import get_current_user
from app.decorators.auth import auth_required

router = APIRouter(
    prefix="/accounts", tags=["Accounts"], dependencies=[Depends(get_current_user)]
)


@router.get("/secure-endpoint")
async def secure_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"안녕하세요 {current_user['username']}님!",
        "user_id": current_user["id"],
        "uuid": current_user["uuid"],
    }


@router.get("/me")
@auth_required()
async def who_am_i(request: Request):
    user = request.state.user
    if not user:
        return {"authenticated": False}

    return {"authenticated": True, "user": user}


@router.post("/internal/cache-invalidate-role/")
async def invalidate_user_cache(payload: dict, request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {settings.INTERNAL_API_KEY}":
        raise HTTPException(status_code=403, detail="Unauthorized")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id missing")

    await redis.delete(f"user:{user_id}")
    return {"status": "cache cleared"}
