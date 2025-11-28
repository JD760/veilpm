from datetime import datetime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import TIMESTAMP, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column


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
