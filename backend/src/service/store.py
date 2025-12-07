from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from src.repository.store import store_repo
from src.db.models import Store
from src.schema.store import StoreCreate, StoreUpdate


class StoreService:
    async def get_stores(self, db: AsyncSession) -> Sequence[Store]:
        return await store_repo.get_all(db)

    async def get_store(self, db: AsyncSession, store_id: UUID) -> Store:
        store = await store_repo.get_by_id(db, store_id)
        if not store:
            raise ValueError("Store not found")
        return store

    async def create_store(self, db: AsyncSession, store_in: StoreCreate) -> Store:
        store = Store(**store_in.model_dump())
        return await store_repo.create(db, store)

    async def update_store(self, db: AsyncSession, store_id: UUID, store_in: StoreUpdate) -> Store:
        values = store_in.model_dump(exclude_unset=True)
        return await store_repo.update(db, store_id, values)

    async def delete_store(self, db: AsyncSession, store_id: UUID) -> None:
        await store_repo.delete(db, store_id)


store_service = StoreService()
