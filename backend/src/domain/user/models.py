from src.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Boolean, TIMESTAMP, UUID as SQL_UUID
from uuid import UUID
from datetime import datetime


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
