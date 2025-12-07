from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Product
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


ProductService = ProductService()