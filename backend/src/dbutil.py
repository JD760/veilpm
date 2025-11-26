from typing import Optional
from urllib.parse import quote

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import sessionmaker, Session

from src.tables.user import DbUser

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
    uri = (
        f"postgresql+psycopg://"
        f":{quote(settings.postgres_password.get_secret_value())}"
        f"@{settings.database_host}"
        f"/{settings.database_name}"
    )
    return uri


def query_db_for_user(session: Session, user_name: str) -> DbUser:
    return session.execute(
        select(DbUser).where(DbUser.name == user_name)
    ).scalar_one_or_none()
