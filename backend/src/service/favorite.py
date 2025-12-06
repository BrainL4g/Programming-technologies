from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from src.repository.favorite import favorite_repo
from src.db.models import Product


class FavoriteService:
    async def add_to_favorites(self, db: AsyncSession, user_id: int, product_id: int) -> None:
        product_exists = await db.execute(select(Product.id).where(Product.id == product_id))
        if not product_exists.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Product not found")

        already_exists = await favorite_repo.exists(db, user_id, product_id)
        if already_exists:
            raise HTTPException(status_code=400, detail="Product already in favorites")

        await favorite_repo.add(db, user_id, product_id)

    async def remove_from_favorites(self, db: AsyncSession, user_id: int, product_id: int) -> None:
        already_exists = await favorite_repo.exists(db, user_id, product_id)
        if not already_exists:
            raise HTTPException(status_code=404, detail="Product not in favorites")

        await favorite_repo.remove(db, user_id, product_id)

    async def get_favorites(self, db: AsyncSession, user_id: int):
        return await favorite_repo.get_user_favorites(db, user_id)


favorite_service = FavoriteService()