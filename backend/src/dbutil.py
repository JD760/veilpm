from functools import wraps
import logging
from typing import Optional
from urllib.parse import quote
from fastapi import Request
from psycopg import AsyncConnection, AsyncCursor, sql
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import TupleRow, dict_row, DictRow, tuple_row, AsyncRowFactory
from .settings import Settings
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

engine: Optional[Engine] = None
sessionLocal: Optional[sessionmaker] = None

def init_database(settings):
    # This should be evil but is actually recommended for handling a session factory
    global engine, sessionLocal
    engine = create_engine(get_connection_uri(settings))
    sessionLocal = sessionmaker(bind=engine)

def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()

class DatabaseServices:
    pool: AsyncConnectionPool


def get_connection_uri(settings: Settings):
    return f"postgresql+psycopg://{settings.postgres_user}:{settings.postgres_password.get_secret_value()}@{settings.database_host}/{settings.database_name}"

async def create_connection_pool(settings: Settings) -> AsyncConnectionPool:
    user_spec = f"{settings.postgres_user}:{quote(settings.postgres_password.get_secret_value())}"
    connection_uri: str = (
        f"postgresql://{user_spec}@{settings.database_host}/{settings.database_name}"
    )
    try:
        return AsyncConnectionPool(connection_uri)
    except:
        raise


async def get_conn(request: Request):
    state = request.app.state
    pool: AsyncConnectionPool = state.database_services.pool
    async with pool.connection() as conn:
        yield conn
