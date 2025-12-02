from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.pre_start import backend_pre_start
from src.utils.mock_data import mocking_data
from src.db.database import SessionLocal

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация бд, таблиц
    await backend_pre_start(app)
    # Удаление данных и загрузка моковых
    await mocking_data()
    yield
    # Выполняется при остановке
    pass


def initialize_backend_application() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app: FastAPI = initialize_backend_application()

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )