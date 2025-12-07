from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Offer, PriceHistory
from src.repository.offer import offer_repo
from src.schema.offer import OfferCreate, OfferUpdate


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


offer_service = OfferService()
