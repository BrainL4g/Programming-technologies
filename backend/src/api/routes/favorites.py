from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import get_current_user
from src.service.favorite import favorite_service
from src.schema.favorite import FavoriteProductResponse
from src.db.models import User

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.post("/{product_id}", status_code=status.HTTP_201_CREATED)
async def add_to_favorites(
    product_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    await favorite_service.add_to_favorites(db, current_user.id, product_id)
    return {"message": "Product added to favorites"}


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def remove_from_favorites(
    product_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    await favorite_service.remove_from_favorites(db, current_user.id, product_id)
    return {"message": "Product removed from favorites"}


@router.get("/", response_model=List[FavoriteProductResponse])
async def get_my_favorites(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    favorites = await favorite_service.get_favorites(db, current_user.id)
    return favorites