from datetime import timedelta

import redis.asyncio as redis
from src.core.config import settings
from src.db.redis_client.redis import pool


class RedisService:
    def __init__(self) -> None:
        self.session = redis.Redis(connection_pool=pool)

    async def create_reset_code(self, email: str, code: str) -> str:
        key = f"reset_code:{email}"
        await self.session.setex(
            key, timedelta(minutes=settings.EMAIL_RESET_CODE_EXP), code
        )
        return code

    async def get_reset_code(self, email: str) -> str:
        key = f"reset_code:{email}"
        return await self.session.get(key)

    async def delete_reset_code(self, email: str):
        key = f"reset_code:{email}"
        await self.session.delete(key)

    async def blacklist_token(self, access_token: str):
        key = f"access_token:{access_token}"
        ttl = timedelta(minutes=settings.JWT_ACCESS_EXP)
        await self.session.setex(key, ttl, access_token)

    async def is_token_blacklisted(self, access_token: str) -> bool:
        key = f"access_token:{access_token}"
        token = await self.session.get(key)
        return token == access_token


redis_service = RedisService()
