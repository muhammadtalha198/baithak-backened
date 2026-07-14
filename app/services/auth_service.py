from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.app_config import AppConfig
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.utils.security import hash_password, verify_password


class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def _require_config() -> None:
    if not settings.DATABASE_URL:
        raise AuthError("Server misconfigured: DATABASE_URL is not set", 503)
    if not settings.JWT_SECRET:
        raise AuthError("Server misconfigured: JWT_SECRET is not set", 503)


async def register_user(db: AsyncSession, data: RegisterRequest) -> User:
    _require_config()
    email = str(data.email).lower() if data.email else None
    phone = data.phone

    filters = []
    if email:
        filters.append(User.email == email)
    if phone:
        filters.append(User.phone == phone)

    existing = await db.execute(select(User).where(or_(*filters)))
    if existing.scalar_one_or_none():
        raise AuthError("An account with this email or phone already exists", 409)

    config_result = await db.execute(
        select(AppConfig).where(AppConfig.id == 1).with_for_update()
    )
    config = config_result.scalar_one_or_none()
    if config is None:
        config = AppConfig(id=1, registration_count=0)
        db.add(config)
        await db.flush()

    registration_number = config.registration_count + 1
    config.registration_count = registration_number

    user = User(
        name=data.name.strip(),
        email=email,
        phone=phone,
        password_hash=hash_password(data.password),
        registration_number=registration_number,
        early_bird_discount=registration_number <= settings.EARLY_BIRD_LIMIT,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def login_user(db: AsyncSession, data: LoginRequest) -> User:
    _require_config()
    email = str(data.email).lower() if data.email else None
    phone = data.phone

    if email:
        result = await db.execute(select(User).where(User.email == email))
    else:
        result = await db.execute(select(User).where(User.phone == phone))

    user = result.scalar_one_or_none()
    if user is None or not verify_password(data.password, user.password_hash):
        raise AuthError("Invalid email/phone or password", 401)
    if not user.is_active:
        raise AuthError("Account is inactive", 403)
    return user


async def get_user_by_id(db: AsyncSession, user_id) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
