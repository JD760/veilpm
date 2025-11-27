from typing import Optional
from sqlalchemy import Engine, create_engine, select, URL
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
    return URL.create(
        drivername="postgresql+psycopg",
        username=settings.postgres_user,
        password=settings.postgres_password.get_secret_value(),
        host=settings.database_host,
        port=settings.database_port,
        database="veil"
    )


def query_db_for_user(session: Session, user_name: str) -> DbUser:
    return session.execute(
        select(DbUser).where(DbUser.name == user_name)
    ).scalar_one_or_none()


def insert_user(session: Session, user: DbUser):
    session.add(user)
    session.commit()
    session.refresh(user)
