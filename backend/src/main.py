from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from src.core.db import init_database, init_in_memory_database
from src.domain import user, auth, vault


@asynccontextmanager
async def lifespan(app: FastAPI):  # pyright: ignore
    init_database()
    yield


@asynccontextmanager
async def mock_lifespan(app: FastAPI):
    init_in_memory_database()
    yield


def create_app(test=False):
    if test:
        app = FastAPI(lifespan=mock_lifespan)
    else:
        app = FastAPI(lifespan=lifespan)  # pyright: ignore
    app.include_router(user.router)
    app.include_router(auth.router)
    app.include_router(vault.router)

    @app.get(
        "/",
        summary="Healthcheck",
        description="Check if the service is running",
    )
    async def healthcheck():
        return {"status": "The service is up"}

    return app


app = create_app()
