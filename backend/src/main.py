from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from .dbutil import init_database
from .routers import auth, user, vault
from .settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = Settings()  # pyright: ignore
    init_database(app.state.settings)
    yield


app = FastAPI(lifespan=lifespan)  # pyright: ignore
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(vault.router)


@app.get(
    "/",
    summary="Healthcheck",
    description="Check if the service is running",
)
async def healthcheck():
    return {"status": "The service is up"}
