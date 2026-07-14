# app/dependencies.py
from collections.abc import AsyncGenerator

import redis.asyncio as redis

from baithak.config import settings

_redis: redis.Redis | None = None


async def init_redis() -> None:
    global _redis
    if not settings.REDIS_URL:
        return
    try:
        client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        await client.ping()
        _redis = client
    except Exception:
        _redis = None


async def close_redis() -> None:
    global _redis
    if _redis:
        await _redis.close()
        _redis = None


async def get_redis() -> AsyncGenerator[redis.Redis | None, None]:
    yield _redis
