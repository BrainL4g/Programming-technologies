import asyncio
import os
import sys
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import joinedload, selectinload

from backend.src.core.config import settings
from backend.src.core.security import get_password_hash
from backend.src.db.database import Base, SessionLocal, engine
from backend.src.db.models import (Category, Favorite, Feature, Product,
                                   Storelink, User)
from backend.src.pre_start import init_models


async def insert_test_data(session: AsyncSession):
    """Вставка тестовых данных в базу"""

    # =============== 1. СОЗДАЕМ ПОЛЬЗОВАТЕЛЕЙ ===============
    user1 = User(
        email="ivan@example.com", password="hashed_password_123", username="ivan_ivanov"
    )

    user2 = User(
        email="anna@example.com",
        password="hashed_password_456",
        username="anna_petrova",
    )

    session.add_all([user1, user2])
    await session.commit()
    await session.refresh(user1)
    await session.refresh(user2)

    # =============== 2. СОЗДАЕМ КАТЕГОРИИ ===============
    electronics = Category(name="Электроника", description="Электронные устройства")
    computers = Category(name="Компьютеры", description="Компьютеры и комплектующие")
    smartphones = Category(name="Смартфоны", description="Мобильные телефоны")

    # Подкатегории
    laptops = Category(
        name="Ноутбуки", description="Портативные компьютеры", parent=computers
    )

    tablets = Category(
        name="Планшеты", description="Планшетные компьютеры", parent=electronics
    )

    session.add_all([electronics, computers, smartphones, laptops, tablets])
    await session.commit()

    # =============== 3. СОЗДАЕМ ПРОДУКТЫ ===============
    product1 = Product(
        name="MacBook Pro 16",
        description="Мощный ноутбук для профессионалов",
        brand="Apple",
    )

    product2 = Product(
        name="iPhone 15 Pro", description="Флагманский смартфон", brand="Apple"
    )

    product3 = Product(
        name="Samsung Galaxy S24", description="Андроид смартфон", brand="Samsung"
    )

    # Привязываем категории к продуктам
    product1.categories = [computers, laptops]
    product2.categories = [electronics, smartphones]
    product3.categories = [electronics, smartphones]

    session.add_all([product1, product2, product3])
    await session.commit()

    # =============== 4. СОЗДАЕМ ХАРАКТЕРИСТИКИ ===============
    feature1 = Feature(name="Оперативная память", unit="ГБ", product_id=product1.id)

    feature2 = Feature(name="Диагональ экрана", unit="дюймов", product_id=product1.id)

    feature3 = Feature(name="Объем памяти", unit="ГБ", product_id=product2.id)

    session.add_all([feature1, feature2, feature3])
    await session.commit()

    # =============== 5. СОЗДАЕМ ССЫЛКИ НА МАГАЗИНЫ ===============
    storelink1 = Storelink(
        url="https://store.apple.com/macbook-pro",
        price=249999.99,
        storename="Apple Store",
        product_id=product1.id,
    )

    storelink2 = Storelink(
        url="https://citilink.ru/macbook-pro",
        price=239999.00,
        storename="Ситилинк",
        product_id=product1.id,
    )

    storelink3 = Storelink(
        url="https://mvideo.ru/iphone-15",
        price=119999.50,
        storename="М.Видео",
        product_id=product2.id,
    )

    session.add_all([storelink1, storelink2, storelink3])
    await session.commit()

    # =============== 6. СОЗДАЕМ ИЗБРАННОЕ ===============
    favorite1 = Favorite(user_id=user1.id, product_id=product1.id, notificate=True)

    favorite2 = Favorite(user_id=user2.id, product_id=product2.id, notificate=False)

    session.add_all([favorite1, favorite2])
    await session.commit()


async def run_select_queries(session: AsyncSession):
    """Выполнение SELECT запросов для тестирования"""

    print("=" * 60)
    print("ВЫПОЛНЕНИЕ SELECT ЗАПРОСОВ")
    print("=" * 60)

    # 1. Все пользователи
    print("\n1. ВСЕ ПОЛЬЗОВАТЕЛИ:")
    print("-" * 40)
    result = await session.execute(select(User))
    users = result.scalars().all()
    for user in users:
        print(
            f"User: id={user.id}, email={user.email}, username={user.username}, fav_products={user.fav_products}"
        )

    # 2. Все продукты с категориями
    print("\n2. ВСЕ ПРОДУКТЫ С КАТЕГОРИЯМИ:")
    print("-" * 40)
    result = await session.execute(select(Product).options())
    products = result.scalars().all()
    for product in products:
        category_names = [cat.name for cat in product.categories]
        print(
            f"Product: id={product.id}, name={product.name}, categories={category_names}, features={product.features}, storelinks={product.storelinks}"
        )

    # 3. Продукты конкретного пользователя
    print("\n3. ПРОДУКТЫ ПОЛЬЗОВАТЕЛЯ IVAN:")
    print("-" * 40)
    result = await session.execute(select(User).where(User.email == "ivan@example.com"))
    user = result.scalar_one()
    for fav in user.fav_products:
        print(f"Product: {fav.name} (ID: {fav.id})")

    # 4. Категории с продуктами
    print("\n4. КАТЕГОРИИ С ПРОДУКТАМИ:")
    print("-" * 40)
    result = await session.execute(
        select(Category).where(Category.name.in_(["Электроника", "Смартфоны"]))
    )
    categories = result.scalars().all()
    for category in categories:
        product_names = [p.name for p in category.products]
        print(f"Category: {category.name} -> Products: {product_names}")

    # 5. Иерархия категорий
    print("\n5. ИЕРАРХИЯ КАТЕГОРИЙ:")
    print("-" * 40)
    result = await session.execute(
        select(Category).options(selectinload(Category.children))
    )
    all_categories = result.scalars().all()
    for cat in all_categories:
        parent_name = cat.parent.name if cat.parent else "None"
        child_names = [c.name for c in cat.children]
        print(f"Category: {cat.name}, Parent: {parent_name}, Children: {child_names}")

    # 6. Ссылки на магазины с ценами
    print("\n6. ЦЕНЫ НА ПРОДУКТЫ В МАГАЗИНАХ:")
    print("-" * 40)
    result = await session.execute(select(Storelink).order_by(Storelink.price))
    storelinks = result.scalars().all()
    for link in storelinks:
        print(f"{link.product.name}: {link.storename} - {link.price} руб.")

    # 7. Избранное пользователей
    print("\n7. ИЗБРАННОЕ ПОЛЬЗОВАТЕЛЕЙ:")
    print("-" * 40)
    result = await session.execute(select(Favorite))
    favorites = result.unique().scalars().all()
    for fav in favorites:
        print(
            f"Favorite #{fav.id}: User={fav.owner.email}, Notify={fav.notificate}, Product = {fav.fav_product}"
        )

    # Средняя цена по магазинам
    result = await session.execute(
        select(Storelink.storename, func.avg(Storelink.price).label("avg_price"))
        .group_by(Storelink.storename)
        .order_by(func.avg(Storelink.price).desc())
    )
    price_stats = result.all()
    for store, avg_price in price_stats:
        print(f"Store {store}: average price = {avg_price:.2f} руб.")

    # 9. Полная информация о продуктах
    print("\n9. ПОЛНАЯ ИНФОРМАЦИЯ О ПРОДУКТАХ:")
    print("-" * 40)

    result = await session.execute(select(Product).order_by(Product.name))
    all_products = result.scalars().all()

    for product in all_products:
        print(f"\n📦 {product.name} ({product.brand})")
        print(f"   Описание: {product.description}")
        print(f"   Категории: {[c.name for c in product.categories]}")
        if product.features:
            print(f"   Характеристики:")
            for feat in product.features:
                print(f"     • {feat.name} ({feat.unit})")
        if product.storelinks:
            print(f"   Магазины:")
            for store in product.storelinks:
                print(f"     • {store.storename}: {store.price} руб.")
        else:
            print(f"   Магазины: нет данных")


async def create_admin_user():
    async with SessionLocal() as db:
        # Check if the admin user already exists
        stmt = select(User).filter(User.is_superuser == True).limit(1)
        result = await db.execute(stmt)
        admin_exists = result.scalar_one_or_none()

        if not admin_exists:
            # Create a new admin user
            password = get_password_hash("12345")  # Set a default password
            new_admin = User(
                email="admin@example.com",
                username="admin",
                password=password,
                is_superuser=True,
            )
            db.add(new_admin)
            await db.commit()
            await db.refresh(new_admin)
            print("Админ admin@example.com с паролем 12345 создан.")


async def mocking_data():
    engine.echo = False
    async with engine.begin() as conn:
        print("Очищение данных")
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        await insert_test_data(session)
        await create_admin_user()
        print("Загружены тестовые данные")
        # await run_select_queries(session)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(mocking_data())
