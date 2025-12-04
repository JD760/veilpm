from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from src.core.db import init_database
from src.domain import user, auth, vault


@asynccontextmanager
async def lifespan(app: FastAPI):  # pyright: ignore
    init_database()
    yield


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
