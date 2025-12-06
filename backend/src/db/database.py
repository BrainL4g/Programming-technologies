from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from backend.src.core.config import settings
import redis

engine = create_async_engine(str(settings.DATABASE_URL), echo=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


def create_redis():
    return redis.ConnectionPool(
        host="localhost", port=6379, db=0, decode_responses=True
    )
