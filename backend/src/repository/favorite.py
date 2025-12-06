from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, exists
from typing import Sequence

from src.db.models import Favorite, Product


class FavoriteRepository:
    async def add(self, db: AsyncSession, user_id: int, product_id: int) -> Favorite:
        favorite = Favorite(user_id=user_id, product_id=product_id)
        db.add(favorite)
        await db.commit()
        await db.refresh(favorite)
        return favorite

    async def remove(self, db: AsyncSession, user_id: int, product_id: int) -> None:
        await db.execute(
            delete(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.product_id == product_id
            )
        )
        await db.commit()

    async def exists(self, db: AsyncSession, user_id: int, product_id: int) -> bool:
        result = await db.execute(
            select(exists().where(
                Favorite.user_id == user_id,
                Favorite.product_id == product_id
            ))
        )
        return result.scalar_one()

    async def get_user_favorites(self, db: AsyncSession, user_id: int) -> Sequence[Product]:
        result = await db.execute(
            select(Product)
            .join(Favorite, Favorite.product_id == Product.id)
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
        )
        return result.scalars().all()


favorite_repo = FavoriteRepository()