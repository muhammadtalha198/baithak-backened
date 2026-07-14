# baithak/database.py
from collections.abc import AsyncGenerator
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from baithak.config import settings


def normalize_database_url(url: str) -> str:
    """Convert Neon/Vercel postgres URLs to SQLAlchemy asyncpg format."""
    if not url:
        return url

    url = url.strip().strip('"').strip("'")
    if url.startswith("postgres://"):
        url = "postgresql+asyncpg://" + url[len("postgres://") :]
    elif url.startswith("postgresql://"):
        url = "postgresql+asyncpg://" + url[len("postgresql://") :]

    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.pop("channel_binding", None)
    if query.get("sslmode"):
        query["ssl"] = query.pop("sslmode")
    if "ssl" not in query:
        query["ssl"] = "require"

    return urlunparse(parsed._replace(query=urlencode(query)))


engine = None
AsyncSessionLocal = None

_db_url = normalize_database_url(settings.DATABASE_URL)
if _db_url:
    engine = create_async_engine(
        _db_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=1,
        max_overflow=0,
    )
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if AsyncSessionLocal is None:
        raise RuntimeError("DATABASE_URL is not configured")
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
