import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.db.database import SessionLocal
from src.db.models import Base, User, Product, Store
from src.core.security import create_access_token

from src.db.redis_client.service import redis_service
redis_service.session = None

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with AsyncSessionLocal() as session:
        yield session


app.dependency_overrides[SessionLocal] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    async def run():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(run())
    yield
    async def drop():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    asyncio.run(drop())


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def user_token():
    import uuid
    email = f"user_{uuid.uuid4()}@test.com"
    async with AsyncSessionLocal() as db:
        user = User(email=email, username="testuser", password="hashed")
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return {"access_token": create_access_token(str(user.id)), "user_id": user.id}


@pytest_asyncio.fixture
async def authenticated_client(client: AsyncClient, user_token):
    client.headers.update({"Authorization": f"Bearer {user_token['access_token']}"})
    yield client
    client.headers.clear()


@pytest_asyncio.fixture
async def admin_token():
    import uuid
    email = f"admin_{uuid.uuid4()}@test.com"
    async with AsyncSessionLocal() as db:
        admin = User(email=email, password="hashed", is_superuser=True)
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
        return {"access_token": create_access_token(str(admin.id))}


@pytest_asyncio.fixture
async def admin_client(client: AsyncClient, admin_token):
    client.headers.update({"Authorization": f"Bearer {admin_token['access_token']}"})
    yield client
    client.headers.clear()


@pytest_asyncio.fixture
async def product_id():
    async with AsyncSessionLocal() as db:
        product = Product(name="iPhone 16", description="New", brand="Apple")
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product.id


@pytest_asyncio.fixture
async def store_id(admin_client):
    resp = await admin_client.post("/stores/", json={"name": "Test DNS", "domain": "test-dns.ru"})
    assert resp.status_code == 201, f"Failed to create store: {resp.text}"
    return resp.json()["id"]