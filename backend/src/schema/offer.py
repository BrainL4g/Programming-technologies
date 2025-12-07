from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, AnyUrl, ConfigDict


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
