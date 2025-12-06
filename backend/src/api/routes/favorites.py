from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.api.dependecies.database import get_db_session
from src.api.dependecies.user import get_current_user
from src.db.models import User, Product, Favorite
from src.schema.favorite import FavoriteProductResponse
from sqlalchemy import select, delete

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.post("/{product_id}", status_code=status.HTTP_201_CREATED)
async def add_to_favorites(
    product_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    # Проверяем, существует ли товар
    product_result = await db.execute(select(Product).where(Product.id == product_id))
    product = product_result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Проверяем, не добавлен ли уже
    fav_result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.product_id == product_id
        )
    )
    if fav_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already in favorites"
        )

    # Добавляем
    favorite = Favorite(user_id=current_user.id, product_id=product_id)
    db.add(favorite)
    await db.commit()
    return {"message": "Product added to favorites"}


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def remove_from_favorites(
    product_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        delete(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.product_id == product_id
        ).returning(Favorite.id)
    )
    deleted = result.scalar_one_or_none()

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not in favorites"
        )

    await db.commit()
    return {"message": "Product removed from favorites"}


@router.get("/", response_model=List[FavoriteProductResponse])
async def get_my_favorites(
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    await db.refresh(current_user, ["fav_products"])
    return current_user.fav_products