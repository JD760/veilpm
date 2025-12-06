from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from .models import DbVault, DbVaultUser
from .schema import Vault, VaultUser
from src.core.db import Queries


class RequestRepository:
    def get_vaults_by_user(
        self,
        session: Session,
        user_id: UUID,
    ) -> list[Vault]:
        # return [Vault.model_validate(row) for row in rows]
        rows = Queries.get_by_field(session, DbVault, "owner", user_id)
        return [Vault.model_validate(row) for row in rows]

    def get_shared_vaults(
        self,
        session: Session,
        user_id: UUID,
    ) -> list[Vault]:
        rows = Queries.get_by_field(
            session,
            DbVaultUser,
            "user_id",
            user_id,
        )
        associations = [VaultUser.model_validate(row) for row in rows]
        db_vaults = [
            Queries.get_by_id(session, DbVault, a.vault_id) for a in associations
        ]
        vaults = [Vault.model_validate(db_vault) for db_vault in db_vaults]
        return vaults

    def share_vault(
        self,
        session: Session,
        vault_id: UUID,
        share_user_id: UUID,
    ) -> DbVaultUser:
        association = DbVaultUser(id=uuid4(), vault_id=vault_id, user_id=share_user_id)
        Queries.insert(session, association)
        return association

    def get_vault_by_id(self, session: Session, vault_id: UUID) -> DbVault:
        return Queries.get_by_id(session, DbVault, vault_id)

    def create_vault(self, session: Session, vault: DbVault):
        Queries.insert(session, vault)

    def delete_vault(self, session: Session, vault_id: UUID):
        Queries.delete_by_id(session, DbVault, vault_id)
