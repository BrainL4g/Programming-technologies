from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes.auth import router as auth_router
from src.api.routes.users import router as user_router
from src.exceptions import register_auth_exception_handlers
from src.pre_start import backend_pre_start
from src.utils.mock_data import mocking_data
from src.api.routes.favorites import router as favorites_router
from src.api.routes.stores import router as stores_router
from src.api.routes.offers import router as offers_router
from src.api.routes.reports import router as reports_router


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
    app.include_router(favorites_router)
    app.include_router(stores_router, prefix="/api/v1")
    app.include_router(offers_router, prefix="/api/v1")
    app.include_router(reports_router, prefix="/api/v1")

    register_auth_exception_handlers(app)

    return app


app: FastAPI = initialize_backend_application()

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
