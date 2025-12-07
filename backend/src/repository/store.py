from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import Sequence

from src.db.models import Store


class StoreRepository:
    async def get_all(self, db: AsyncSession) -> Sequence[Store]:
        result = await db.execute(select(Store).order_by(Store.name))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, store_id: UUID) -> Store | None:
        result = await db.execute(select(Store).where(Store.id == store_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, store: Store) -> Store:
        db.add(store)
        await db.commit()
        await db.refresh(store)
        return store

    async def update(self, db: AsyncSession, store_id: UUID, values: dict) -> Store:
        await db.execute(update(Store).where(Store.id == store_id).values(**values))
        await db.commit()
        result = await db.execute(select(Store).where(Store.id == store_id))
        return result.scalar_one()

    async def delete(self, db: AsyncSession, store_id: UUID) -> None:
        await db.execute(delete(Store).where(Store.id == store_id))
        await db.commit()

store_repo = StoreRepository()
