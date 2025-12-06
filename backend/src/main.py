from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.exceptions import register_auth_exception_handlers
from backend.src.pre_start import backend_pre_start
from backend.src.utils.mock_data import mocking_data
from backend.src.api.routes.auth import router as auth_router
from backend.src.api.routes.users import router as user_router
from backend.src.db.database import SessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация бд, таблиц
    await backend_pre_start(app)
    # Удаление данных и загрузка моковых, админа
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

    app.include_router(auth_router)
    app.include_router(user_router)

    register_auth_exception_handlers(app)

    return app


app: FastAPI = initialize_backend_application()

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
