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
import random
from decimal import Decimal
from datetime import datetime, timedelta

async def generate_fake_history(session, offer, days=30):
    """
    Генерирует историю цен для оффера без ошибок типов данных.
    """
    history_entries = []
    
    # Приводим к Decimal для совместимости с Numeric(12, 2)
    base_price = Decimal(str(offer.price))
    current_price = base_price + Decimal(random.randint(2000, 8000))
    
    # Идем от прошлого к настоящему
    start_date = datetime.utcnow() - timedelta(days=days)

    for i in range(days):
        # Вероятность изменения цены 25%
        if random.random() < 0.25:
            # Генерация волатильности: изменение на -2%...1.5%
            change_percent = random.uniform(-0.02, 0.015)
            current_price = current_price * Decimal(str(1 + change_percent))
            
            # Ограничитель: цена не может упасть ниже 70% от текущей
            min_allowed = base_price * Decimal('0.7')
            if current_price < min_allowed:
                current_price = min_allowed

        # Создаем запись
        date_for_entry = start_date + timedelta(days=i)
        
        history_item = PriceHistory(
            offer_id=offer.id,
            price=round(current_price, 2),
            recorded_at=date_for_entry
        )
        history_entries.append(history_item)

    # Добавляем финальную актуальную точку
    history_entries.append(PriceHistory(
        offer_id=offer.id,
        price=base_price,
        recorded_at=datetime.utcnow()
    ))
    
    session.add_all(history_entries)
    await session.commit()

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

    electronics = Category(name="Электроника", description="desc")
    c2 = Category(name="Инструменты", description="desc")
    c3 = Category(name="Комплектующие", description="desc")
    c4 = Category(name="Красота и здоровье", description="desc")
    c5 = Category(name="Фототехника", description="desc")
    smartphones = Category(name="Смартфоны", description="desc")
    laptops = Category( name="Ноутбуки", description="desc")

    session.add_all([electronics, c2, c3, c4, c5, smartphones, laptops])
    await session.commit()

    for cat in [electronics, c2, c3, c4, c5, smartphones, laptops]:
        await session.refresh(cat)
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
        file_url="src/../static/products/1.jpg",
        product_id=product1.id
    )

    attachment2 = Attachment(
        file_url="src/../static/products/2.webp",
        product_id=product1.id
    )

    attachment3 = Attachment(
        file_url="src/../static/products/3.webp",
        product_id=product2.id
    )

    attachment7 = Attachment(
    file_url="src/../static/products/4.jpg",
    product_id=product2.id
    )

    attachment8 = Attachment(
    file_url="src/../static/products/5.jpg",
    product_id=product3.id
    )

    attachment9 = Attachment(
    file_url="src/../static/products/6.jpg",
    product_id=product3.id
    )

    session.add_all([attachment1, attachment2, attachment3, attachment7, attachment8, attachment9])
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

    offer4 = Offer(
        product_id=product3.id,
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

    session.add_all([offer1, offer2, offer3, offer4])
    await session.commit()

    for offer in [offer1, offer2, offer3, offer4]:
        await session.refresh(offer)

    await generate_fake_history(session, offer1, days=60)
    await generate_fake_history(session, offer2, days=60)
    await generate_fake_history(session, offer3, days=60)
    await generate_fake_history(session, offer4, days=60)

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

    # 1. Google Pixel 8 Pro
    product_pixel = Product(
        name="Google Pixel 8 Pro",
        description="Смартфон с лучшей камерой и чистым Android",
        brand="Google",
        category_id=smartphones.id,
        specifications={
            "processor": "Google Tensor G3",
            "ram": "12GB",
            "storage": "128GB",
            "camera": "50MP + 48MP + 48MP"
        }
    )

    # 2. Xiaomi 14 Ultra
    product_xiaomi = Product(
        name="Xiaomi 14 Ultra",
        description="Ультимативный флагман с оптикой Leica",
        brand="Xiaomi",
        category_id=smartphones.id,
        specifications={
            "processor": "Snapdragon 8 Gen 3",
            "ram": "16GB",
            "storage": "512GB",
            "camera": "50MP (1 inch sensor)"
        }
    )

    # 3. Samsung Galaxy Z Fold5
    product_fold = Product(
        name="Samsung Galaxy Z Fold5",
        description="Складной смартфон для продуктивности",
        brand="Samsung",
        category_id=smartphones.id,
        specifications={
            "processor": "Snapdragon 8 Gen 2",
            "ram": "12GB",
            "storage": "256GB",
            "Дисплей": "7.6 inch Dynamic AMOLED"
        }
    )

    session.add_all([product_pixel, product_xiaomi, product_fold])
    await session.commit()
    
    for p in [product_pixel, product_xiaomi, product_fold]:
        await session.refresh(p)

    attachments_extra = [
        Attachment(file_url="src/../static/products/10.jpg", product_id=product_pixel.id),
        Attachment(file_url="src/../static/products/11.jpg", product_id=product_xiaomi.id),
        Attachment(file_url="src/../static/products/12.png", product_id=product_fold.id),
    ]
    session.add_all(attachments_extra)

    offer_pixel = Offer(
        product_id=product_pixel.id,
        external_id="mvideo-pixel8-001",
        store_id=store3.id, 
        price=95000.00,
        old_price=105000.00,
        currency="RUB",
        available=True,
        in_stock=15,
        url="https://mvideo.ru/google-pixel-8-pro",
        image_url="https://mvideo.ru/images/pixel8.jpg"
    )

    offer_xiaomi = Offer(
        product_id=product_xiaomi.id,
        external_id="citilink-xiaomi14-001",
        store_id=store2.id, # Ситилинк
        price=125000.00,
        old_price=139000.00,
        currency="RUB",
        available=True,
        in_stock=3,
        url="https://citilink.ru/xiaomi-14-ultra",
        image_url="https://citilink.ru/images/xiaomi14.jpg"
    )

    offer_fold = Offer(
        product_id=product_fold.id,
        external_id="apple-fold-001", 
        store_id=store1.id, 
        price=155000.00,
        old_price=170000.00,
        currency="RUB",
        available=True,
        in_stock=5,
        url="https://store.apple.com/samsung-fold-5",
        image_url="https://store.apple.com/images/fold5.jpg"
    )

    session.add_all([offer_pixel, offer_xiaomi, offer_fold])
    await session.commit()

    for o in [offer_pixel, offer_xiaomi, offer_fold]:
        await session.refresh(o)
        await generate_fake_history(session, o, days=45)

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
