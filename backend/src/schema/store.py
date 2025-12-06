from datetime import datetime
from uuid import UUID
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, AnyUrl


class StoreBase(BaseModel):
    name: str = Field(..., max_length=100)
    domain: str = Field(..., max_length=255)
    is_active: Optional[bool] = True


class StoreCreate(StoreBase):
    pass


class StoreUpdate(StoreBase):
    name: Optional[str] = None
    domain: Optional[str] = None
    is_active: Optional[bool] = None


class StoreResponse(StoreBase):
    id: UUID
    last_sync: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OfferBase(BaseModel):
    price: float
    old_price: Optional[float] = None
    currency: str = "RUB"
    available: bool = True
    in_stock: int = 0
    product_id: int
    url: AnyUrl


class OfferCreate(OfferBase):
    store_id: UUID


class OfferUpdate(BaseModel):
    price: Optional[float] = None
    old_price: Optional[float] = None
    available: Optional[bool] = None
    in_stock: Optional[int] = None
    url: Optional[AnyUrl] = None


class OfferResponse(OfferBase):
    id: UUID
    store_id: UUID
    last_updated: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PriceHistoryResponse(BaseModel):
    id: UUID
    price: float
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)