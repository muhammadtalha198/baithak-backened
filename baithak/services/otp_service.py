# app/services/otp_service.py
import hashlib
import json
import secrets

import redis.asyncio as redis

from baithak.config import settings

OTP_KEY_PREFIX = "otp:pending:"
MAX_ATTEMPTS = 5

def generate_otp() -> str:
    """Cryptographically secure 6-digit OTP."""
    return "".join(str(secrets.randbelow(10)) for _ in range(6))

def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()

def _key(identifier: str) -> str:
    return f"{OTP_KEY_PREFIX}{identifier}"

async def store_pending_registration(
    redis_client: redis.Redis,
    identifier: str,
    otp: str,
    password_hash: str,
) -> None:
    record = {
        "hash": hash_otp(otp),
        "password_hash": password_hash,
        "attempts": 0,
    }
    await redis_client.set(
        _key(identifier),
        json.dumps(record),
        ex=settings.OTP_EXPIRE_SECONDS,
    )

async def get_pending(redis_client: redis.Redis, identifier: str) -> dict | None:
    data = await redis_client.get(_key(identifier))
    if not data:
        return None
    return json.loads(data)

async def verify_otp(
    redis_client: redis.Redis,
    identifier: str,
    otp: str,
) -> dict:
    """
    Returns pending record on success.
    Raises ValueError for invalid/expired/max attempts.
    """
    record = await get_pending(redis_client, identifier)
    if not record:
        raise ValueError("OTP_EXPIRED")

    record["attempts"] = record.get("attempts", 0) + 1
    if record["attempts"] > MAX_ATTEMPTS:
        await redis_client.delete(_key(identifier))
        raise ValueError("OTP_MAX_ATTEMPTS")

    if hash_otp(otp) != record["hash"]:
        await redis_client.set(
            _key(identifier),
            json.dumps(record),
            ex=settings.OTP_EXPIRE_SECONDS,
        )
        raise ValueError("OTP_INVALID")

    return record

async def delete_pending(redis_client: redis.Redis, identifier: str) -> None:
    await redis_client.delete(_key(identifier))