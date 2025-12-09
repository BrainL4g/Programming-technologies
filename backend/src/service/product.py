from typing import Any, Dict, List, Optional, Sequence
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Product, PriceHistory
from src.repository.product import ProductCrud
from src.schema.product import ProductCreate, ProductUpdate


class ProductService:
    async def create_product(self, db: AsyncSession, product_data: ProductCreate) -> Product:
        return await ProductCrud.create_product(product_data.model_dump(), db)

    async def get_product_by_id(self, db: AsyncSession, product_id: int) -> Product:
        product = await ProductCrud.get_product_by_id(product_id, db)
        if not product:
            raise ValueError("Product not found")
        return product

    async def get_products(self, db: AsyncSession, skip: int, limit: int) -> List[Product]:
        return await ProductCrud.get_products(db, skip, limit)
    
    async def get_products_with_filters(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 10,
        category_id: Optional[int] = None,
        brand: Optional[str] = None,
        specifications: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc"
    ) -> List[Product]:
        products = await ProductCrud.get_products_with_filters(
            db, skip, limit, category_id, brand, specifications, sort_by, sort_order
        )
        
        # Рассчитываем min_price и max_price для каждого продукта
        for product in products:
            if product.offers:
                prices = [offer.price for offer in product.offers if offer.available]
                if prices:
                    product.min_price = min(prices)
                    product.max_price = max(prices)
        
        return list(products)

    async def update_product(
            self, db: AsyncSession, product: Product, update_data: ProductUpdate
    ) -> Product:
        return await ProductCrud.update_product(
            product, update_data.model_dump(exclude_unset=True), db
        )

    async def delete_product(self, db: AsyncSession, product_id: int) -> None:
        try:
            await ProductCrud.delete_product(product_id, db)
        except ValueError:
            raise ValueError("Product not found")
        
    async def get_product_prices(
        self,
        db: AsyncSession,
        product_id: int
    ) -> Dict[str, Any]:
        # Проверка существования
        product = await ProductCrud.get_product_by_id(product_id, db)
        if not product:
            raise ValueError("Product not found")
        
        # Получаем текущую среднюю цену
        current_avg_price = await ProductCrud.get_product_average_price(db, product_id)
        
        # Получаем историю средних цен (последние 30 дней)
        price_history = await ProductCrud.get_product_average_price_history(db, product_id, days_limit=30)
        
        # Форматируем историю для ответа
        formatted_history = [
            {
                'date': entry['date'].isoformat(),
                'average_price': entry['average_price']
            }
            for entry in price_history
        ]
        
        return {
            'product_id': product_id,
            'current_average_price': current_avg_price,
            'price_history': formatted_history
        }


ProductService = ProductService()