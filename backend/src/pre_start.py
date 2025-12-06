
import asyncpg
from fastapi import FastAPI

from backend.src.core.config import settings
from backend.src.db.database import Base, engine
from backend.src.db.models import *


async def check_db_connection():
    db_config = {
        "user": settings.DATABASE_USER,
        "password": settings.DATABASE_PASSWORD,
        "host": settings.DATABASE_HOST,
        "port": settings.DATABASE_PORT,
        "database": "postgres",
    }

    db_name = "tp"

    try:
        try:
            conn = await asyncpg.connect(**db_config)
            print("Подключение к серверу PostgreSQL успешно")
        except asyncpg.exceptions.ConnectionDoesNotExistError:
            print("PostgreSQL сервер недоступен")
            return False
        try:
            exists = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1", db_name
            )

            if not exists:
                await conn.execute(f"CREATE DATABASE {db_name}")
                print(f"База данных '{db_name}' создана")

                await conn.execute(
                    f"""
                    ALTER DATABASE {db_name} SET timezone TO 'UTC';
                    ALTER DATABASE {db_name} SET client_encoding TO 'UTF8';
                """
                )
            else:
                print(f"База данных '{db_name}' уже существует")

            await conn.close()

            db_config["database"] = db_name
            test_conn = await asyncpg.connect(**db_config)

            db_info = await test_conn.fetchval("SELECT current_database()")
            print(f"Подключение к базе данных '{db_info}' успешно")

            await test_conn.close()
            return True

        except Exception as e:
            await conn.close()
            print(f"Ошибка при работе с БД: {e}")
            return False

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        return False


async def init_models():
    async with engine.begin() as conn:
        print("Создание таблиц")
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        print("Таблицы созданы")


async def backend_pre_start(app: FastAPI):
    engine.echo = False
    success = await check_db_connection()

    if success:
        pass
    else:
        print("Не удалось подключиться к базе данных")
    await init_models()
