from sqlalchemy import select
from uuid import UUID, uuid4
from .models import DbVault, DbVaultUser
from .schema import Vault, VaultUser
from src.core.db import Queries
from src.core.repositories.crud_repository import CrudRepository


class VaultRepository(CrudRepository):
    def __init__(self, session):
        super().__init__(session, DbVault)
        self.session = session

    def get_vaults_by_user(
        self,
        user_id: UUID,
    ) -> list[Vault]:
        # return [Vault.model_validate(row) for row in rows]
        rows = Queries.get_by_field(self.session, DbVault, "owner", user_id)
        return [Vault.model_validate(row) for row in rows]

    def get_shared_vaults(
        self,
        user_id: UUID,
    ) -> list[Vault]:
        rows = Queries.get_by_field(
            self.session,
            DbVaultUser,
            "user_id",
            user_id,
        )
        associations = [VaultUser.model_validate(row) for row in rows]
        db_vaults = [
            Queries.get_by_id(
                self.session,
                DbVault,
                a.vault_id,
            )
            for a in associations
        ]
        vaults = [Vault.model_validate(db_vault) for db_vault in db_vaults]
        return vaults

    def share_vault(
        self,
        vault_id: UUID,
        share_user_id: UUID,
    ) -> DbVaultUser:
        association = DbVaultUser(
            id=uuid4(),
            vault_id=vault_id,
            user_id=share_user_id,
        )
        Queries.insert(self.session, association)
        return association

    def unshare_vault(
        self,
        vault_id: UUID,
        share_user_id: UUID,
    ):
        association = (
            self.session.execute(
                select(DbVaultUser).where(
                    DbVaultUser.vault_id == vault_id,
                    DbVaultUser.user_id == share_user_id,
                )
            )
            .scalars()
            .one_or_none()
        )
        Queries.delete(self.session, association)

    def get_vault_by_id(self, vault_id: UUID) -> DbVault:
        return Queries.get_by_id(self.session, DbVault, vault_id)

    def create_vault(self, vault: DbVault):
        Queries.insert(self.session, vault)

    def delete_vault(self, vault_id: UUID):
        Queries.delete_by_id(self.session, DbVault, vault_id)
