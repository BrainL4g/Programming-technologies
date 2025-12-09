from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import get_current_active_superuser
from src.schema.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from src.schema.price import ProductPricesResponse
from src.service.product import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
        product_data: ProductCreate,
        db: AsyncSession = Depends(get_db_session),
        admin = Depends(get_current_active_superuser)
):
    return await ProductService.create_product(db, product_data)


@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    brand: Optional[str] = Query(None),
    specifications: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    sort_order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db_session),
):
        return await ProductService.get_products_with_filters(
            db=db,
            skip=skip,
            limit=limit,
            category_id=category_id,
            brand=brand,
            specifications=specifications,
            sort_by=sort_by,
            sort_order=sort_order
        )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
        product_id: int,
        db: AsyncSession = Depends(get_db_session),
):
    return await ProductService.get_product_by_id(db, product_id)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
        product_id: int,
        update_data: ProductUpdate,
        db: AsyncSession = Depends(get_db_session),
        admin = Depends(get_current_active_superuser),
):
    product = await ProductService.get_product_by_id(db, product_id)
    return await ProductService.update_product(db, product, update_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_id: int,
        db: AsyncSession = Depends(get_db_session),
        admin = Depends(get_current_active_superuser),
):
    await ProductService.delete_product(db, product_id)


@router.get("/{product_id}/prices", response_model=ProductPricesResponse)
async def get_product_prices(
    product_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    return await ProductService.get_product_prices(db, product_id)