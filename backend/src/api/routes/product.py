from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import get_current_active_superuser
from src.schema.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
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
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db_session),
):
    return await ProductService.get_products(db, skip, limit)


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