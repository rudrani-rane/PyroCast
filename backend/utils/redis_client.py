"""Redis client factory."""

import redis.asyncio as aioredis

from backend.config.settings import get_settings

_redis_client: aioredis.Redis[str] | None = None


async def get_redis_client() -> aioredis.Redis[str]:
    """Return a shared async Redis client instance."""
    global _redis_client
    if _redis_client is None:
        settings = get_settings()
        _redis_client = aioredis.from_url(
            str(settings.redis_url),
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client


async def close_redis_client() -> None:
    """Close the shared Redis client connection."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None
