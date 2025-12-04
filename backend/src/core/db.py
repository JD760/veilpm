from typing import Optional
from sqlalchemy import Engine, create_engine, URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.core.config import settings

engine: Optional[Engine] = None
sessionLocal: Optional[sessionmaker] = None


# Base class for database models
class Base(DeclarativeBase):
    pass


def init_database():
    global engine, sessionLocal
    engine = create_engine(get_connection_uri())
    sessionLocal = sessionmaker(bind=engine)
    print("Database initialised!")


def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_connection_uri():
    return URL.create(
        drivername="postgresql+psycopg",
        username=settings.postgres_user,
        password=settings.postgres_password.get_secret_value(),
        host=settings.database_host,
        port=settings.database_port,
        database="veil",
    )
