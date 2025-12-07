from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Category
from src.repository.category import CategoryCrud
from src.schema.category import CategoryCreate, CategoryUpdate


class CategoryService:
    async def create_category(self, db: AsyncSession, category_data: CategoryCreate) -> Category:
        return await CategoryCrud.create_category(category_data.model_dump(), db)

    async def get_category_by_id(self, db: AsyncSession, category_id: int) -> Category:
        category = await CategoryCrud.get_category_by_id(category_id, db)
        if not category:
            raise ValueError("Category not found")
        return category

    async def get_categories(self, db: AsyncSession, skip: int, limit: int) -> List[Category]:
        return await CategoryCrud.get_categories(db, skip, limit)

    async def update_category(
            self, db: AsyncSession, category: Category, update_data: CategoryUpdate
    ) -> Category:
        return await CategoryCrud.update_category(
            category, update_data.model_dump(exclude_unset=True), db
        )

    async def delete_category(self, db: AsyncSession, category_id: int) -> None:
        try:
            await CategoryCrud.delete_category(category_id, db)
        except ValueError:
            raise ValueError("Category not found")

    async def get_category_tree(self, db: AsyncSession) -> List[Category]:
        return await CategoryCrud.get_category_tree(db)


CategoryService = CategoryService()