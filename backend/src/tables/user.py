from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Boolean, Column, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Base(DeclarativeBase):
    pass

class DbUser(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "users"}
    name: Mapped[str] = mapped_column(Text, primary_key=True)
    email: Mapped[str] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean)
    creation_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    last_login: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    password_hash: Mapped[str | None] = mapped_column(Text)
    