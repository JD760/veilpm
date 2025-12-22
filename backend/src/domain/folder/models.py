from uuid import UUID
from src.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID as SQL_UUID


class DbFolder(Base):
    __tablename__ = "folder"
    __table_args__ = {"schema": "veil"}
    id: Mapped[UUID] = mapped_column(SQL_UUID, primary_key=True)
    folder_id: Mapped[UUID] = mapped_column(SQL_UUID)
    vault_id: Mapped[UUID] = mapped_column(SQL_UUID)
