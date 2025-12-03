from datetime import datetime
from uuid import UUID
from src.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import TIMESTAMP, UUID as SQL_UUID, Text, select

from src.models.vault import Vault


class DbVault(Base):
    __tablename__ = "vault"
    __table_args__ = {"schema": "veil"}
    id: Mapped[UUID] = mapped_column(SQL_UUID, primary_key=True)
    owner: Mapped[UUID] = mapped_column(SQL_UUID, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    creation_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    passphrase_hash: Mapped[str] = mapped_column(Text)


class _Queries:
    # TODO: Generalise these get by ID operations etc.
    @staticmethod
    def get_vault_by_id(session: Session, vault_id: UUID):
        return (
            session.execute(select(DbVault).where(DbVault.id == vault_id))
            .scalars()
            .one_or_none()
        )

    @staticmethod
    def delete_vault(session: Session, vault_id: UUID):
        vault = get_vault_by_id(session, vault_id)
        session.delete(vault)
        session.commit()
        session.refresh(vault)

    @staticmethod
    def get_vaults_by_user(session: Session, user_id: UUID):
        return session.execute(
            select(DbVault).where(DbVault.owner == user_id)
        ).scalars()

    @staticmethod
    def create_vault(session: Session, vault: DbVault):
        session.add(vault)
        session.commit()
        session.refresh(vault)


def get_vaults_by_user(session: Session, user_id: UUID) -> list[Vault]:
    rows = _Queries.get_vaults_by_user(session, user_id)
    return [Vault.model_validate(row) for row in rows]


def get_vault_by_id(session: Session, vault_id: UUID) -> DbVault:
    return _Queries.get_vault_by_id(session, vault_id)


def create_vault(session: Session, vault: DbVault):
    _Queries.create_vault(session, vault)


def delete_vault(session: Session, vault_id: UUID):
    _Queries.delete_vault(session, vault_id)
