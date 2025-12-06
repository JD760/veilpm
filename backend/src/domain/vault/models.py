from src.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, TIMESTAMP, UUID as SQL_UUID
from uuid import UUID
from datetime import datetime


class DbVault(Base):
    __tablename__ = "vault"
    __table_args__ = {"schema": "veil"}
    id: Mapped[UUID] = mapped_column(SQL_UUID, primary_key=True)
    owner: Mapped[UUID] = mapped_column(SQL_UUID, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    creation_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    passphrase_hash: Mapped[str] = mapped_column(Text)


class DbVaultUser(Base):
    __tablename__ = "vault_user"
    __table_args__ = {"schema": "veil"}
    id: Mapped[UUID] = mapped_column(SQL_UUID, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(SQL_UUID)
    vault_id: Mapped[UUID] = mapped_column(SQL_UUID)
