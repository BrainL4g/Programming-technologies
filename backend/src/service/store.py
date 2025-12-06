from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from src.repository.store import store_repo, offer_repo
from src.db.models import Store, Offer, PriceHistory
from src.schema.store import StoreCreate, StoreUpdate, OfferCreate, OfferUpdate


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


class OfferService:
    async def get_offers(self, db: AsyncSession, **filters) -> Sequence[Offer]:
        return await offer_repo.get_all(db, **filters)

    async def get_offer(self, db: AsyncSession, offer_id: UUID) -> Offer:
        offer = await offer_repo.get_by_id(db, offer_id)
        if not offer:
            raise ValueError("Offer not found")
        return offer

    async def create_offer(self, db: AsyncSession, offer_in: OfferCreate) -> Offer:
        offer = Offer(**offer_in.model_dump())
        return await offer_repo.create(db, offer)

    async def update_offer(self, db: AsyncSession, offer_id: UUID, offer_in: OfferUpdate) -> Offer:
        values = offer_in.model_dump(exclude_unset=True)
        return await offer_repo.update(db, offer_id, values)

    async def delete_offer(self, db: AsyncSession, offer_id: UUID) -> None:
        await offer_repo.delete(db, offer_id)

    async def get_price_history(self, db: AsyncSession, offer_id: UUID) -> Sequence[PriceHistory]:
        return await offer_repo.get_price_history(db, offer_id)


store_service = StoreService()
offer_service = OfferService()