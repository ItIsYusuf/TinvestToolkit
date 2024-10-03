import redis.asyncio as aioredis
from src.adapters.cache.settings import Settings

settings = Settings()

async def get_redis_client():
    redis = await aioredis.from_url(
        settings.REDIS_URL,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        encoding="utf-8",
        decode_response=True
    )
    return redis