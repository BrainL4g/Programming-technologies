from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


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
