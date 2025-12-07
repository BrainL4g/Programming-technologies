from typing import List, Any, Coroutine, Sequence

import sqlalchemy
from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.models import Product


class ProductCRUDRepository:
    async def create_product(self, product_data: dict, db: AsyncSession) -> Product:
        product = Product(**product_data)
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    async def get_product_by_id(self, product_id: int, db: AsyncSession) -> Product:
        stmt = select(Product).where(Product.id == product_id)
        query = await db.execute(stmt.options(
            selectinload(Product.category),
            selectinload(Product.category),
            selectinload(Product.offers),
            selectinload(Product.images),
        ))
        return query.scalar_one_or_none()

    async def get_products(self, db: AsyncSession, skip: int, limit: int) -> Sequence[Product]:
        stmt = select(Product).offset(skip).limit(limit)
        query = await db.execute(stmt.options(
            selectinload(Product.category),
            selectinload(Product.category),
            selectinload(Product.offers),
            selectinload(Product.images),
        ))
        return query.scalars().all()

    async def update_product(self, product: Product, update_data: dict, db: AsyncSession) -> Product:
        for key, value in update_data.items():
            setattr(product, key, value)
        await db.commit()
        return product

    async def delete_product(self, product_id: int, db: AsyncSession) -> None:
        stmt = select(Product).where(Product.id == product_id)
        query = await db.execute(stmt)
        product = query.scalar_one_or_none()

        if product is None:
            raise ValueError(f"Product with id {product_id} does not exist.")

        await db.delete(product)
        await db.commit()


ProductCrud = ProductCRUDRepository()