from typing import Optional, Type, TypeVar
from uuid import UUID
from sqlalchemy import Engine, create_engine, URL, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy_memory import MemorySession
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


def init_in_memory_database():
    global engine, sessionLocal
    engine = create_engine("memory://")
    sessionLocal = sessionmaker(
        bind=engine,
        class_=MemorySession,
        expire_on_commit=False,
    )


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


T = TypeVar("T", bound=Base)


class Queries:
    def get_by_id(session: Session, model: Type[T], id: UUID) -> T:
        return (
            session.execute(select(model).where(model.id == id)).scalars().one_or_none()
        )

    def get_by_field(
        session: Session,
        model: Type[T],
        field_name: str,
        field_value,
    ) -> list[T]:
        field = getattr(model, field_name)
        return (
            session.execute(select(model).where(field == field_value)).scalars().all()
        )

    def get_one_by_field(
        session: Session,
        model: Type[T],
        field_name: str,
        field_value,
    ) -> T:
        rows = Queries.get_by_field(session, model, field_name, field_value)
        if len(rows) != 1:
            return None
        return rows

    def insert(session: Session, row: T):
        session.add(row)
        session.commit()
        session.refresh(row)

    def delete(session, row: T):
        session.delete(row)
        session.commit()

    def delete_by_id(session, model: Type[T], id: UUID):
        row = Queries.get_by_id(session, model, id)
        Queries.delete(session, row)
