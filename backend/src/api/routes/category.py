from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.dependecies.database import get_db_session
from src.schema.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryResponseTree
from src.service.category import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
        category_data: CategoryCreate,
        db: AsyncSession = Depends(get_db_session),
):
    return await CategoryService.create_category(db, category_data)


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db_session),
):
    return await CategoryService.get_categories(db, skip, limit)

@router.get("/tree", response_model=List[CategoryResponseTree])
async def get_category_tree(
        db: AsyncSession = Depends(get_db_session)
):
    return await CategoryService.get_category_tree(db)

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
        category_id: int,
        db: AsyncSession = Depends(get_db_session),
):
    return await CategoryService.get_category_by_id(db, category_id)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
        category_id: int,
        update_data: CategoryUpdate,
        db: AsyncSession = Depends(get_db_session),
):
    category = await CategoryService.get_category_by_id(db, category_id)
    return await CategoryService.update_category(db, category, update_data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_id: int,
        db: AsyncSession = Depends(get_db_session),
):
    await CategoryService.delete_category(db, category_id)

