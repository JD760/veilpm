from typing import Optional

from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import sessionmaker

from .settings import Settings

engine: Optional[Engine] = None
sessionLocal: Optional[sessionmaker] = None


def init_database(settings):
    # This should be evil but is actually recommended
    # for handling a session factory
    global engine, sessionLocal
    engine = create_engine(get_connection_uri(settings))
    sessionLocal = sessionmaker(bind=engine)


def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_connection_uri(settings: Settings):
    return URL.create(
        drivername="postgresql+psycopg",
        username=settings.postgres_user,
        password=settings.postgres_password.get_secret_value(),
        host=settings.database_host,
        port=settings.database_port,
        database="veil",
    )
