# app/services/rate_limit.py
import redis.asyncio as redis

from app.config import settings

async def check_rate_limit(
    redis_client: redis.Redis,
    key: str,
    limit: int,
    window_seconds: int,
) -> bool:
    """Returns True if under limit, False if rate limited."""
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key, window_seconds)
    return count <= limit

async def is_register_allowed(redis_client: redis.Redis, ip: str) -> bool:
    key = f"rate:register:{ip}"
    return await check_rate_limit(
        redis_client, key,
        settings.RATE_LIMIT_REGISTER_PER_IP,
        3600,
    )

async def is_otp_send_allowed(redis_client: redis.Redis, identifier: str) -> bool:
    key = f"rate:otp:{identifier}"
    return await check_rate_limit(
        redis_client, key,
        settings.RATE_LIMIT_OTP_PER_IDENTIFIER,
        900,
    )