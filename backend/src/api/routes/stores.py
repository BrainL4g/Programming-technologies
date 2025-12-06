from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List
from uuid import UUID

from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import get_current_active_superuser
from src.db.models import Store, Offer, PriceHistory
from src.schema.store import (
    StoreCreate, StoreUpdate, StoreResponse,
    OfferCreate, OfferUpdate, OfferResponse,
    PriceHistoryResponse
)

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("/", response_model=List[StoreResponse])
async def get_stores(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Store).order_by(Store.name))
    return result.scalars().all()


@router.get("/{store_id}", response_model=StoreResponse)
async def get_store(store_id: UUID, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Store).where(Store.id == store_id))
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(
    store_in: StoreCreate,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser)
):
    store = Store(**store_in.model_dump())
    db.add(store)
    await db.commit()
    await db.refresh(store)
    return store


@router.put("/{store_id}", response_model=StoreResponse)
async def update_store(
    store_id: UUID,
    store_in: StoreUpdate,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser)
):
    await db.execute(
        update(Store)
        .where(Store.id == store_id)
        .values(**store_in.model_dump(exclude_unset=True))
    )
    await db.commit()
    result = await db.execute(select(Store).where(Store.id == store_id))
    return result.scalar_one()


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_store(
    store_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser)
):
    await db.execute(delete(Store).where(Store.id == store_id))
    await db.commit()


@router.get("/{store_id}/offers/", response_model=List[OfferResponse])
async def get_store_offers(store_id: UUID, db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(Offer)
        .where(Offer.store_id == store_id)
        .order_by(Offer.last_updated.desc())
    )
    return result.scalars().all()


@router.post("/{store_id}/sync/", status_code=status.HTTP_202_ACCEPTED)
async def trigger_sync(
    store_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db_session),
    _: None = Depends(get_current_active_superuser)
):
    result = await db.execute(select(Store).where(Store.id == store_id))
    store = result.scalar_one_or_none()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    background_tasks.add_task(sync_store_offers, store_id)
    return {"detail": "Sync started"}


async def sync_store_offers(store_id: UUID):
    # Здесь будет вызов парсера/скрапера
    pass