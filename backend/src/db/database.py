import redis
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

from src.core.config import settings

engine = create_async_engine(str(settings.DATABASE_URL), echo=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


def create_redis():
    return redis.ConnectionPool(
        host="localhost", port=6379, db=0, decode_responses=True
    )
