from datetime import datetime
from fastapi import Depends, HTTPException
from http import HTTPStatus
from src.core.db import get_session
from src.core.security import PasswordHandler
from src.domain.folder.service import get_folder_service
from src.domain.user.schema import User
from .schema import CreateVault, Vault, VaultUser
from .repository import VaultRepository
from uuid import UUID, uuid4
from .models import DbVault


def get_vault_service(session=Depends(get_session)):
    return VaultService(session)


class VaultService:
    def __init__(self, session):
        self.session = session
        self._repository: VaultRepository = VaultRepository(session)

    def get_vaults_by_user(self, user_id: UUID):
        return self._repository.get_vaults_by_user(user_id)

    def get_shared_vaults(self, user_id: UUID) -> list[Vault]:
        return self._repository.get_shared_vaults(user_id)

    def get_vault_folders(self, vault_id, user_id: UUID):
        vault: Vault = Vault.model_validate(
            self._repository.get_by_id(vault_id),
        )
        vault.check_ownership(user_id)
        folder_service = get_folder_service(self.session)
        return folder_service.get_vault_folders(vault_id)

    def create_vault(self, vault_create: CreateVault, user_id: UUID):
        db_vault: DbVault = DbVault(
            id=uuid4(),
            owner=user_id,
            name=vault_create.name,
            description=vault_create.description,
            creation_date=datetime.now(),
            passphrase_hash=PasswordHandler.hash(vault_create.passphrase),
        )
        self._repository.create(db_vault)
        return Vault.model_validate(db_vault)

    def share_vault_with_user(
        self,
        vault_id: UUID,
        user: User,
        shared_user_id: UUID,
    ) -> VaultUser:
        vault: Vault = self.get_vault_by_id(vault_id, user.id)
        vault.check_ownership(user.id)
        return VaultUser.model_validate(
            self._repository.share_vault(vault.id, shared_user_id)
        )

    def unshare_vault_with_user(
        self,
        vault_id: UUID,
        user: User,
        shared_user_id: UUID,
    ):
        vault: Vault = self.get_vault_by_id(vault_id, user.id)
        vault.check_ownership(user.id)
        self._repository.unshare_vault(
            vault_id,
            shared_user_id,
        )

    def get_vault_by_id(self, vault_id: UUID, user_id: UUID) -> Vault:
        db_vault: DbVault = self._repository.get_by_id(
            vault_id,
        )
        if not db_vault:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Vault not found")
        vault: Vault = Vault.model_validate(db_vault)
        vault.check_ownership(user_id)
        return self._repository.get_by_id(vault_id)

    def delete_vault(self, vault_id: UUID, user_id: UUID):
        db_vault = self.get_vault_by_id(vault_id)
        if not db_vault:
            raise HTTPException(
                HTTPStatus.NOT_FOUND,
                f"Vault {vault_id} does not exist",
            )
        vault: Vault = Vault.model_validate(db_vault)
        vault.check_ownership(user_id)
        return self._repository.delete(vault)
