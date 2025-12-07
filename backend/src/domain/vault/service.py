from datetime import datetime
from fastapi import HTTPException
from http import HTTPStatus
from src.core.security import PasswordHandler
from src.domain.user.schema import User
from .schema import CreateVault, Vault, VaultUser
from .repository import RequestRepository
from uuid import UUID, uuid4
from .models import DbVault


class VaultService:
    def __init__(self, repository):
        self._repository: RequestRepository = repository

    def get_vaults_by_user(self, session, user_id: UUID):
        return self._repository.get_vaults_by_user(session, user_id)

    def get_shared_vaults(self, session, user_id: UUID) -> list[Vault]:
        return self._repository.get_shared_vaults(session, user_id)

    def create_vault(self, session, vault_create: CreateVault, user_id: UUID):
        db_vault: DbVault = DbVault(
            id=uuid4(),
            owner=user_id,
            name=vault_create.name,
            description=vault_create.description,
            creation_date=datetime.now(),
            passphrase_hash=PasswordHandler.hash(vault_create.passphrase),
        )
        self._repository.create_vault(session, db_vault)
        return Vault.model_validate(db_vault)

    def share_vault_with_user(
        self, session, vault_id: UUID, user: User, shared_user_id: UUID
    ) -> VaultUser:
        vault: Vault = self.get_vault_by_id(session, vault_id, user.id)
        self._check_vault_ownership(vault, user.id)
        return VaultUser.model_validate(
            self._repository.share_vault(session, vault.id, shared_user_id)
        )

    def unshare_vault_with_user(
        self,
        session,
        vault_id: UUID,
        user: User,
        shared_user_id: UUID,
    ):
        vault: Vault = self.get_vault_by_id(session, vault_id, user.id)
        self._check_vault_ownership(vault, user.id)
        self._repository.unshare_vault(
            session,
            vault_id,
            shared_user_id,
        )

    def get_vault_by_id(self, session, vault_id: UUID, user_id: UUID) -> Vault:
        db_vault: DbVault = self._repository.get_vault_by_id(
            session,
            vault_id,
        )
        if not db_vault:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Vault not found")
        vault: Vault = Vault.model_validate(db_vault)
        self._check_vault_ownership(vault, user_id)
        return self._repository.get_vault_by_id(session, vault_id)

    def delete_vault(self, session, vault_id: UUID, user_id: UUID):
        db_vault = vault_service.get_vault_by_id(session, vault_id)
        if not db_vault:
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                f"Vault {vault_id} does not exist",
            )
        vault: Vault = Vault.model_validate(db_vault)
        self._check_vault_ownership(vault, user_id)
        return self._repository.delete_vault(session, vault)

    @staticmethod
    def _check_vault_ownership(vault: Vault, user_id: UUID) -> None:
        if vault.owner != user_id:
            raise HTTPException(
                HTTPStatus.UNAUTHORIZED, "Only the owner may modify a vault"
            )


vault_service = VaultService(RequestRepository())
