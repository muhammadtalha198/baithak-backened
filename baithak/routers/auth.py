from fastapi import APIRouter, Depends, HTTPException, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from baithak.dependencies import get_redis
from baithak.database import get_db
from baithak.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserResponse
from baithak.services.auth_service import AuthError, get_user_by_id, login_user, register_user
from baithak.services.rate_limits import is_register_allowed
from baithak.utils.jwt import create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _auth_response(user) -> AuthResponse:
    return AuthResponse(
        access_token=create_access_token(user.id),
        user=UserResponse.model_validate(user),
    )


@router.post("/register", response_model=AuthResponse)
async def register(
    body: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    redis: Redis | None = Depends(get_redis),
):
    if redis is not None and not await is_register_allowed(redis, _client_ip(request)):
        raise HTTPException(status_code=429, detail="Too many registration attempts. Try again later.")

    try:
        user = await register_user(db, body)
    except AuthError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Registration failed: {exc}") from exc

    return _auth_response(user)


@router.post("/login", response_model=AuthResponse)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await login_user(db, body)
    except AuthError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return _auth_response(user)


@router.get("/me", response_model=UserResponse)
async def me(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    auth = request.headers.get("authorization", "")
    if not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")

    user_id = decode_access_token(auth.split(" ", 1)[1].strip())
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return UserResponse.model_validate(user)
