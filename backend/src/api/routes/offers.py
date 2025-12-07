from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import get_current_active_superuser
from src.service.offer import offer_service
from src.schema.offer import OfferCreate, OfferUpdate, OfferResponse, PriceHistoryResponse

router = APIRouter(prefix="/offers", tags=["offers"])


@router.get("/", response_model=List[OfferResponse])
async def get_offers(
    db: AsyncSession = Depends(get_db_session),
    store_id: Optional[UUID] = None,
    available: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
):
    return await offer_service.get_offers(
        db,
        store_id=store_id,
        available=available,
        min_price=min_price,
        max_price=max_price,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.get("/{offer_id}", response_model=OfferResponse)
async def get_offer(offer_id: UUID, db: AsyncSession = Depends(get_db_session)):
    return await offer_service.get_offer(db, offer_id)


@router.post("/", response_model=OfferResponse, status_code=status.HTTP_201_CREATED)
async def create_offer(
    offer_in: OfferCreate,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser),
):
    return await offer_service.create_offer(db, offer_in)


@router.put("/{offer_id}", response_model=OfferResponse)
async def update_offer(
    offer_id: UUID,
    offer_in: OfferUpdate,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser),
):
    return await offer_service.update_offer(db, offer_id, offer_in)


@router.patch("/{offer_id}", response_model=OfferResponse)
async def patch_offer(
    offer_id: UUID,
    offer_in: OfferUpdate,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser),
):
    return await offer_service.update_offer(db, offer_id, offer_in)


@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offer(
    offer_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser),
):
    await offer_service.delete_offer(db, offer_id)


@router.get("/{offer_id}/price-history/", response_model=List[PriceHistoryResponse])
async def get_price_history(
    offer_id: UUID,
    db: AsyncSession = Depends(get_db_session),
):
    return await offer_service.get_price_history(db, offer_id)