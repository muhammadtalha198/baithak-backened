# app/dependencies.py
from collections.abc import AsyncGenerator

import redis.asyncio as redis

from app.config import settings

_redis: redis.Redis | None = None

async def init_redis() -> None:
    global _redis
    _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def close_redis() -> None:
    global _redis
    if _redis:
        await _redis.close()

async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    if _redis is None:
        raise RuntimeError("Redis not initialized")
    yield _redis
