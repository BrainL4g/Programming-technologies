from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from uuid import UUID
from typing import List

from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import get_current_active_superuser
from src.service.store import store_service, offer_service
from src.schema.store import StoreCreate, StoreUpdate, StoreResponse, OfferResponse

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("/", response_model=List[StoreResponse])
async def get_stores(db = Depends(get_db_session)):
    return await store_service.get_stores(db)


@router.get("/{store_id}", response_model=StoreResponse)
async def get_store(store_id: UUID, db = Depends(get_db_session)):
    return await store_service.get_store(db, store_id)


@router.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(store_in: StoreCreate, db = Depends(get_db_session), _: None = Depends(get_current_active_superuser)):
    return await store_service.create_store(db, store_in)


@router.put("/{store_id}", response_model=StoreResponse)
async def update_store(store_id: UUID, store_in: StoreUpdate, db = Depends(get_db_session), _: None = Depends(get_current_active_superuser)):
    return await store_service.update_store(db, store_id, store_in)


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_store(store_id: UUID, db = Depends(get_db_session), _: None = Depends(get_current_active_superuser)):
    await store_service.delete_store(db, store_id)


@router.get("/{store_id}/offers/", response_model=List[OfferResponse])
async def get_store_offers(store_id: UUID, db = Depends(get_db_session)):
    return await offer_service.get_offers(db, store_id=store_id)