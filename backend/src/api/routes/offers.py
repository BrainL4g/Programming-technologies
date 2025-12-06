from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional
from uuid import UUID

from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import get_current_active_superuser
from src.db.models import Offer, PriceHistory
from src.schema.store import OfferCreate, OfferUpdate, OfferResponse, PriceHistoryResponse

router = APIRouter(prefix="/offers", tags=["offers"])


@router.get("/", response_model=List[OfferResponse])
async def get_offers(
    db: AsyncSession = Depends(get_db_session),
    store_id: Optional[UUID] = None,
    available: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = Query(None, description="Search in name/brand"),
    skip: int = 0,
    limit: int = 50
):
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


@router.get("/{offer_id}", response_model=OfferResponse)
async def get_offer(offer_id: UUID, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Offer).where(Offer.id == offer_id))
    offer = result.scalar_one_or_none()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer


@router.post("/", response_model=OfferResponse, status_code=status.HTTP_201_CREATED)
async def create_offer(
    offer_in: OfferCreate,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser)
):
    offer = Offer(**offer_in.model_dump())
    db.add(offer)
    await db.commit()
    await db.refresh(offer)
    return offer


@router.put("/{offer_id}", response_model=OfferResponse)
async def update_offer(
    offer_id: UUID,
    offer_in: OfferUpdate,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser)
):
    await db.execute(
        update(Offer)
        .where(Offer.id == offer_id)
        .values(**offer_in.model_dump(exclude_unset=True))
    )
    await db.commit()
    result = await db.execute(select(Offer).where(Offer.id == offer_id))
    return result.scalar_one()


@router.patch("/{offer_id}", response_model=OfferResponse)
async def patch_offer(
    offer_id: UUID,
    offer_in: OfferUpdate,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser)
):
    return await update_offer(offer_id, offer_in, db)


@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offer(
    offer_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser)
):
    await db.execute(delete(Offer).where(Offer.id == offer_id))
    await db.commit()


@router.get("/{offer_id}/price-history/", response_model=List[PriceHistoryResponse])
async def get_price_history(offer_id: UUID, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(PriceHistory)
        .where(PriceHistory.offer_id == offer_id)
        .order_by(PriceHistory.recorded_at.desc())
    )
    return result.scalars().all()