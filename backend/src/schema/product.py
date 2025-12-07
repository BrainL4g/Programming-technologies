from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime
from uuid import UUID

from src.schema.attachment import AttachmentResponse
from src.schema.category import CategoryResponse
from src.schema.offer import OfferResponse
from src.schema.store import StoreResponse


class ProductBase(BaseModel):
    name: str
    description: str
    brand: str
    category_id: int
    specifications: Optional[Dict] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    category_id: Optional[int] = None
    specifications: Optional[Dict] = None


class ProductImage(BaseModel):
    id: int
    file_url: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductOffer(BaseModel):
    id: UUID
    price: float
    old_price: Optional[float] = None
    currency: str
    available: bool
    in_stock: int
    store: StoreResponse
    last_updated: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(ProductBase):
    id: int
    images: List[AttachmentResponse] = []
    category: CategoryResponse
    offers: List[OfferResponse] = []
    min_price: Optional[float] = None
    max_price: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    products: List[ProductResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ProductSearchFilters(BaseModel):
    category_id: Optional[int] = None
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    available: Optional[bool] = True
    search_query: Optional[str] = None


class ProductPaginatedResponse(BaseModel):
    items: List[ProductListResponse]
    total: int
    page: int
    size: int
    pages: int

