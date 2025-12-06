import asyncio
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from src.db.database import Base, SessionLocal, engine
import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import get_password_hash
from src.db.models import (
    User, Category, Product, Favorite,
    Store, Offer, PriceHistory, Attachment
)

async def insert_test_data(session: AsyncSession):
    user1 = User(
        email="ivan@example.com",
        password=get_password_hash("password123"),
        username="ivan_ivanov"
    )

    user2 = User(
        email="anna@example.com",
        password=get_password_hash("password456"),
        username="anna_petrova"
    )


    session.add_all([user1, user2])
    await session.commit()
    await session.refresh(user1)
    await session.refresh(user2)

    electronics = Category(name="Электроника", description="Электронные устройства")
    computers = Category(name="Компьютеры", description="Компьютеры и комплектующие")
    smartphones = Category(name="Смартфоны", description="Мобильные телефоны")

    laptops = Category(
        name="Ноутбуки",
        description="Портативные компьютеры",
        parent_id=None
    )

    tablets = Category(
        name="Планшеты",
        description="Планшетные компьютеры",
        parent_id=None
    )

    session.add_all([electronics, computers, smartphones, laptops, tablets])
    await session.commit()

    for cat in [electronics, computers, smartphones, laptops, tablets]:
        await session.refresh(cat)

    laptops.parent_id = computers.id
    tablets.parent_id = electronics.id
    await session.commit()

    product1 = Product(
        name="MacBook Pro 16",
        description="Мощный ноутбук для профессионалов",
        brand="Apple",
        category_id=laptops.id,
        specifications={
            "processor": "M3 Pro",
            "ram": "18GB",
            "storage": "512GB",
            "display": "16.2"
        }
    )

    product2 = Product(
        name="iPhone 15 Pro",
        description="Флагманский смартфон",
        brand="Apple",
        category_id=smartphones.id,
        specifications={
            "processor": "A17 Pro",
            "ram": "8GB",
            "storage": "256GB",
            "camera": "48MP"
        }
    )

    product3 = Product(
        name="Samsung Galaxy S24",
        description="Андроид смартфон",
        brand="Samsung",
        category_id=smartphones.id,
        specifications={
            "processor": "Snapdragon 8 Gen 3",
            "ram": "12GB",
            "storage": "256GB",
            "camera": "50MP"
        }
    )

    session.add_all([product1, product2, product3])
    await session.commit()

    for prod in [product1, product2, product3]:
        await session.refresh(prod)

    attachment1 = Attachment(
        file_url="https://example.com/images/macbook1.jpg",
        product_id=product1.id
    )

    attachment2 = Attachment(
        file_url="https://example.com/images/macbook2.jpg",
        product_id=product1.id
    )

    attachment3 = Attachment(
        file_url="https://example.com/images/iphone1.jpg",
        product_id=product2.id
    )

    attachment4 = Attachment(
        file_url="https://example.com/icons/electronics.svg",
        category_id=electronics.id
    )

    attachment5 = Attachment(
        file_url="https://example.com/icons/computers.svg",
        category_id=computers.id
    )

    attachment6 = Attachment(
        file_url="https://example.com/icons/smartphones.svg",
        category_id=smartphones.id
    )

    session.add_all([attachment1, attachment2, attachment3, attachment4, attachment5, attachment6])
    await session.commit()

    store1 = Store(
        name="Apple Store",
        domain="store.apple.com",
        is_active=True
    )

    store2 = Store(
        name="Ситилинк",
        domain="citilink.ru",
        is_active=True
    )

    store3 = Store(
        name="М.Видео",
        domain="mvideo.ru",
        is_active=True
    )

    session.add_all([store1, store2, store3])
    await session.commit()

    for store in [store1, store2, store3]:
        await session.refresh(store)

    offer1 = Offer(
        product_id=product1.id,
        external_id="apple-mbp-16-001",
        store_id=store1.id,
        price=249999.99,
        old_price=259999.99,
        currency="RUB",
        available=True,
        in_stock=10,
        url="https://store.apple.com/macbook-pro-16",
        image_url="https://store.apple.com/images/mbp16.jpg"
    )

    offer2 = Offer(
        product_id=product1.id,
        external_id="citilink-mbp-16-001",
        store_id=store2.id,
        price=239999.00,
        old_price=249999.00,
        currency="RUB",
        available=True,
        in_stock=5,
        url="https://citilink.ru/macbook-pro-16",
        image_url="https://citilink.ru/images/mbp16.jpg"
    )

    offer3 = Offer(
        product_id=product2.id,
        external_id="mvideo-iphone15-001",
        store_id=store3.id,
        price=119999.50,
        old_price=129999.50,
        currency="RUB",
        available=True,
        in_stock=20,
        url="https://mvideo.ru/iphone-15-pro",
        image_url="https://mvideo.ru/images/iphone15.jpg"
    )

    session.add_all([offer1, offer2, offer3])
    await session.commit()

    for offer in [offer1, offer2, offer3]:
        await session.refresh(offer)

    price_history1 = PriceHistory(
        offer_id=offer1.id,
        price=259999.99
    )

    price_history2 = PriceHistory(
        offer_id=offer1.id,
        price=249999.99
    )

    price_history3 = PriceHistory(
        offer_id=offer2.id,
        price=249999.00
    )

    price_history4 = PriceHistory(
        offer_id=offer2.id,
        price=239999.00
    )

    price_history5 = PriceHistory(
        offer_id=offer3.id,
        price=129999.50
    )

    price_history6 = PriceHistory(
        offer_id=offer3.id,
        price=119999.50
    )

    session.add_all([
        price_history1, price_history2, price_history3,
        price_history4, price_history5, price_history6
    ])
    await session.commit()

    favorite1 = Favorite(
        user_id=user1.id,
        product_id=product1.id,
        notificate=True
    )

    favorite2 = Favorite(
        user_id=user2.id,
        product_id=product2.id,
        notificate=False
    )

    favorite3 = Favorite(
        user_id=user1.id,
        product_id=product3.id,
        notificate=True
    )

    session.add_all([favorite1, favorite2, favorite3])
    await session.commit()

# async def run_select_queries(session: AsyncSession):
#     """Выполнение SELECT запросов для тестирования"""
#
#     print("=" * 60)
#     print("ВЫПОЛНЕНИЕ SELECT ЗАПРОСОВ")
#     print("=" * 60)
#
#     # 1. Все пользователи
#     print("\n1. ВСЕ ПОЛЬЗОВАТЕЛИ:")
#     print("-" * 40)
#     result = await session.execute(select(User))
#     users = result.scalars().all()
#     for user in users:
#         print(
#             f"User: id={user.id}, email={user.email}, username={user.username}, fav_products={user.fav_products}"
#         )
#
#     # 2. Все продукты с категориями
#     print("\n2. ВСЕ ПРОДУКТЫ С КАТЕГОРИЯМИ:")
#     print("-" * 40)
#     result = await session.execute(select(Product).options())
#     products = result.scalars().all()
#     for product in products:
#         category_names = [cat.name for cat in product.categories]
#         print(
#             f"Product: id={product.id}, name={product.name}, categories={category_names}, features={product.features}, storelinks={product.storelinks}"
#         )
#
#     # 3. Продукты конкретного пользователя
#     print("\n3. ПРОДУКТЫ ПОЛЬЗОВАТЕЛЯ IVAN:")
#     print("-" * 40)
#     result = await session.execute(select(User).where(User.email == "ivan@example.com"))
#     user = result.scalar_one()
#     for fav in user.fav_products:
#         print(f"Product: {fav.name} (ID: {fav.id})")
#
#     # 4. Категории с продуктами
#     print("\n4. КАТЕГОРИИ С ПРОДУКТАМИ:")
#     print("-" * 40)
#     result = await session.execute(
#         select(Category).where(Category.name.in_(["Электроника", "Смартфоны"]))
#     )
#     categories = result.scalars().all()
#     for category in categories:
#         product_names = [p.name for p in category.products]
#         print(f"Category: {category.name} -> Products: {product_names}")
#
#     # 5. Иерархия категорий
#     print("\n5. ИЕРАРХИЯ КАТЕГОРИЙ:")
#     print("-" * 40)
#     result = await session.execute(
#         select(Category).options(selectinload(Category.children))
#     )
#     all_categories = result.scalars().all()
#     for cat in all_categories:
#         parent_name = cat.parent.name if cat.parent else "None"
#         child_names = [c.name for c in cat.children]
#         print(f"Category: {cat.name}, Parent: {parent_name}, Children: {child_names}")
#
#     # 6. Ссылки на магазины с ценами
#     print("\n6. ЦЕНЫ НА ПРОДУКТЫ В МАГАЗИНАХ:")
#     print("-" * 40)
#     result = await session.execute(select(Storelink).order_by(Storelink.price))
#     storelinks = result.scalars().all()
#     for link in storelinks:
#         print(f"{link.product.name}: {link.storename} - {link.price} руб.")
#
#     # 7. Избранное пользователей
#     print("\n7. ИЗБРАННОЕ ПОЛЬЗОВАТЕЛЕЙ:")
#     print("-" * 40)
#     result = await session.execute(select(Favorite))
#     favorites = result.unique().scalars().all()
#     for fav in favorites:
#         print(
#             f"Favorite #{fav.id}: User={fav.owner.email}, Notify={fav.notificate}, Product = {fav.fav_product}"
#         )
#
#     # Средняя цена по магазинам
#     result = await session.execute(
#         select(Storelink.storename, func.avg(Storelink.price).label("avg_price"))
#         .group_by(Storelink.storename)
#         .order_by(func.avg(Storelink.price).desc())
#     )
#     price_stats = result.all()
#     for store, avg_price in price_stats:
#         print(f"Store {store}: average price = {avg_price:.2f} руб.")
#
#     # 9. Полная информация о продуктах
#     print("\n9. ПОЛНАЯ ИНФОРМАЦИЯ О ПРОДУКТАХ:")
#     print("-" * 40)
#
#     result = await session.execute(select(Product).order_by(Product.name))
#     all_products = result.scalars().all()
#
#     for product in all_products:
#         print(f"\n📦 {product.name} ({product.brand})")
#         print(f"   Описание: {product.description}")
#         print(f"   Категории: {[c.name for c in product.categories]}")
#         if product.features:
#             print("   Характеристики:")
#             for feat in product.features:
#                 print(f"     • {feat.name} ({feat.unit})")
#         if product.storelinks:
#             print("   Магазины:")
#             for store in product.storelinks:
#                 print(f"     • {store.storename}: {store.price} руб.")
#         else:
#             print("   Магазины: нет данных")


async def create_admin_user():
    async with SessionLocal() as db:
        # Check if the admin user already exists
        stmt = select(User).filter(User.email == "admin@example.com").limit(1)
        result = await db.execute(stmt)
        admin_exists = result.scalar_one_or_none()

        if not admin_exists:
            print("Админ не найден")
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
        print("Создание админа")
        await create_admin_user()
        print("Загружены тестовые данные")
        # await run_select_queries(session)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(mocking_data())
