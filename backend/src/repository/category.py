from typing import List, Any, Coroutine, Sequence

import sqlalchemy
from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.models import Category


class CategoryCRUDRepository:
    async def create_category(self, category_data: dict, db: AsyncSession) -> Category:
        category = Category(**category_data)
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    async def get_category_by_id(self, category_id: int, db: AsyncSession) -> Category:
        stmt = select(Category).where(Category.id == category_id)
        query = await db.execute(stmt)
        return query.scalar_one_or_none()

    async def get_categories(self, db: AsyncSession, skip: int, limit: int) -> list[Category]:
        stmt = select(Category).offset(skip).limit(limit)
        query = await db.execute(stmt)
        return query.scalars().all()

    async def update_category(
            self, category: Category, update_data: dict, db: AsyncSession
    ) -> Category:
        for key, value in update_data.items():
            setattr(category, key, value)
        await db.commit()
        return category

    async def delete_category(self, category_id: int, db: AsyncSession) -> None:
        stmt = select(Category).where(Category.id == category_id)
        query = await db.execute(stmt)
        category = query.scalar_one_or_none()

        if category is None:
            raise ValueError(f"Category with id {category_id} does not exist.")

        await db.delete(category)
        await db.commit()

    async def get_category_tree(self, db: AsyncSession) -> Sequence[Category]:
        stmt = (
            select(Category)
            .where(Category.parent_id.is_(None))
            .options(
                selectinload(Category.children)
                .selectinload(Category.children)
                .selectinload(Category.children)
            )
            .order_by(Category.name)
        )
        query = await db.execute(stmt)
        return query.scalars().unique().all()

CategoryCrud = CategoryCRUDRepository()