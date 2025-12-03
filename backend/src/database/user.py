from datetime import datetime
from sqlalchemy import TIMESTAMP, Boolean, Text, select, UUID as SQL_UUID
from sqlalchemy.orm import Mapped, mapped_column, Session
from uuid import UUID
from src.database.base import Base


class DbUser(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "veil"}
    id: Mapped[UUID] = mapped_column(SQL_UUID, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean)
    creation_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
    )
    last_login: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
    )
    password_hash: Mapped[str | None] = mapped_column(Text)


class _Queries:
    @staticmethod
    def get_user_by_id(session: Session, user_id: UUID):
        return session.execute(
            select(DbUser).where(DbUser.id == user_id)
        ).scalar_one_or_none()

    def get_user_by_name(session: Session, user_name: str):
        # NOTE: This may fail in future if we support
        # multiple users with the same name
        return session.execute(
            select(DbUser).where(DbUser.name == user_name)
        ).scalar_one_or_none()


def get_user(session: Session, user_id: UUID) -> DbUser:
    return _Queries.get_user_by_id(session, user_id)


def get_user_by_name(session: Session, user_name: str) -> DbUser:
    return _Queries.get_user_by_name(session, user_name)


def insert_user(session: Session, user: DbUser):
    session.add(user)
    session.commit()
    session.refresh(user)


def set_last_login(session: Session, user_id: UUID):
    user: DbUser = _Queries.get_user_by_id(session, user_id)
    session.delete(user)
    user.last_login = datetime.now()
    session.add(user)
    session.commit()
    session.refresh(user)
