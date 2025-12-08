from datetime import datetime
from typing import Dict, List, Any, Coroutine, Optional, Sequence
from uuid import UUID

import sqlalchemy
from sqlalchemy.orm import aliased
from sqlalchemy import Date, Tuple, and_, cast, func, select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.models import Product, PriceHistory, Offer


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

    
    async def get_product_average_price(
        self, 
        db: AsyncSession, 
        product_id: int
    ) -> Optional[float]:
        """Получить текущую среднюю цену товара по всем доступным оферам"""
        stmt = (
            select(func.avg(Offer.price))
            .where(
                Offer.product_id == product_id,
                Offer.available == True
            )
        )
        result = await db.execute(stmt)
        avg_price = result.scalar_one_or_none()
        return float(avg_price) if avg_price else None

    async def get_product_average_price_history(
        self, 
        db: AsyncSession, 
        product_id: int,
        days_limit: int = 30
    ) -> List[Dict[str, any]]:
        """
        Получить историю средних цен товара
        Returns: список словарей с датой и средней ценой
        """
        # Получаем последнюю цену каждого офера за каждый день
        latest_prices_subq = (
            select(
                PriceHistory.offer_id,
                cast(PriceHistory.recorded_at, Date).label('day'),
                func.max(PriceHistory.recorded_at).label('max_recorded_at')
            )
            .join(Offer, Offer.id == PriceHistory.offer_id)
            .where(Offer.product_id == product_id)
            .group_by(PriceHistory.offer_id, cast(PriceHistory.recorded_at, Date))
            .subquery('latest_prices')
        )
        
        # Получаем актуальные цены по этим временным меткам
        price_history_alias = aliased(PriceHistory)
        
        stmt = (
            select(
                latest_prices_subq.c.day,
                func.avg(price_history_alias.price).label('avg_price')
            )
            .join(
                price_history_alias,
                and_(
                    price_history_alias.offer_id == latest_prices_subq.c.offer_id,
                    price_history_alias.recorded_at == latest_prices_subq.c.max_recorded_at
                )
            )
            .group_by(latest_prices_subq.c.day)
            .order_by(latest_prices_subq.c.day.desc())
            .limit(days_limit)
        )
        
        result = await db.execute(stmt)
        rows = result.all()
        
        return [
            {
                'date': row.day,
                'average_price': float(row.avg_price)
            }
            for row in rows
        ]


ProductCrud = ProductCRUDRepository()