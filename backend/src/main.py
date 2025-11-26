from fastapi import Depends, FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.orm import Session
from .tables.user import DbUser
from .routers import auth
from .settings import Settings
from .dbutil import get_session, init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = Settings() # pyright: ignore
    init_database(app.state.settings)
    yield


app = FastAPI(lifespan=lifespan)  # pyright: ignore
app.include_router(auth.router)


@app.get(
    "/",
    summary="Healthcheck",
    description="Check if the service is running",
)
async def healthcheck():
    return {"status": "The service is up"}


@app.get(
    "/db",
    summary="Database access check",
    description="Test fetching something from the database",
)
async def db_check(session: Session = Depends(get_session)):
    users = session.execute(select(DbUser)).scalars().all()
    return {"users": users}