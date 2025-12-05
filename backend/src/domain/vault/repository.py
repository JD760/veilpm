from sqlalchemy.orm import Session
from uuid import UUID
from .models import DbVault
from .schema import Vault
from sqlalchemy import select


class RequestRepository:
    def get_vaults_by_user(
        self,
        session: Session,
        user_id: UUID,
    ) -> list[Vault]:
        rows = self._Queries.get_vaults_by_user(session, user_id)
        return [Vault.model_validate(row) for row in rows]

    def get_vault_by_id(self, session: Session, vault_id: UUID) -> DbVault:
        return self._Queries.get_vault_by_id(session, vault_id)

    def create_vault(self, session: Session, vault: DbVault):
        self._Queries.create_vault(session, vault)

    def delete_vault(self, session: Session, vault_id: UUID):
        self._Queries.delete_vault(session, vault_id)

    class _Queries:
        # TODO: Generalise these get by ID operations etc.
        @classmethod
        def get_vault_by_id(cls, session: Session, vault_id: UUID):
            return (
                session.execute(select(DbVault).where(DbVault.id == vault_id))
                .scalars()
                .one_or_none()
            )

        @classmethod
        def delete_vault(cls, session: Session, vault_id: UUID):
            vault = cls.get_vault_by_id(session, vault_id)
            session.delete(vault)
            session.commit()

        @classmethod
        def get_vaults_by_user(cls, session: Session, user_id: UUID):
            return session.execute(
                select(DbVault).where(DbVault.owner == user_id)
            ).scalars()

        @classmethod
        def create_vault(cls, session: Session, vault: DbVault):
            session.add(vault)
            session.commit()
            session.refresh(vault)
