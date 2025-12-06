import redis.asyncio as redis

from backend.src.db.database import SessionLocal
from backend.src.db.redis_client.redis import pool


async def get_db_session():
    async with SessionLocal() as session:
        yield session


def get_redis_session():
    return redis.Redis(connection_pool=pool)
