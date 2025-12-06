from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import Sequence

from src.db.models import Store, Offer, PriceHistory


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


class OfferRepository:
    async def get_all(
        self,
        db: AsyncSession,
        store_id: UUID | None = None,
        available: bool | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> Sequence[Offer]:
        stmt = select(Offer)
        if store_id:
            stmt = stmt.where(Offer.store_id == store_id)
        if available is not None:
            stmt = stmt.where(Offer.available == available)
        if min_price is not None:
            stmt = stmt.where(Offer.price >= min_price)
        if max_price is not None:
            stmt = stmt.where(Offer.price <= max_price)
        if search:
            stmt = stmt.where(
                (Offer.product_name.ilike(f"%{search}%")) |
                (Offer.brand.ilike(f"%{search}%"))
            )
        stmt = stmt.order_by(Offer.last_updated.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, offer_id: UUID) -> Offer | None:
        result = await db.execute(select(Offer).where(Offer.id == offer_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, offer: Offer) -> Offer:
        db.add(offer)
        await db.commit()
        await db.refresh(offer)
        return offer

    async def update(self, db: AsyncSession, offer_id: UUID, values: dict) -> Offer:
        await db.execute(update(Offer).where(Offer.id == offer_id).values(**values))
        await db.commit()
        result = await db.execute(select(Offer).where(Offer.id == offer_id))
        return result.scalar_one()

    async def delete(self, db: AsyncSession, offer_id: UUID) -> None:
        await db.execute(delete(Offer).where(Offer.id == offer_id))
        await db.commit()

    async def get_price_history(self, db: AsyncSession, offer_id: UUID) -> Sequence[PriceHistory]:
        result = await db.execute(
            select(PriceHistory)
            .where(PriceHistory.offer_id == offer_id)
            .order_by(PriceHistory.recorded_at.desc())
        )
        return result.scalars().all()


store_repo = StoreRepository()
offer_repo = OfferRepository()