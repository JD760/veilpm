from .schema import Vault
from .repository import RequestRepository
from uuid import UUID


class VaultService:
    def __init__(self, repository):
        self._repository: RequestRepository = repository

    def get_vaults_by_user(self, session, user_id: UUID):
        return self._repository.get_vaults_by_user(session, user_id)

    def create_vault(self, session, vault):
        self._repository.create_vault(session, vault)

    def get_vault_by_id(self, session, vault_id: UUID) -> Vault:
        return self._repository.get_vault_by_id(session, vault_id)

    def delete_vault(self, session, vault: UUID):
        return self._repository.delete_vault(session, vault)


vault_service = VaultService(RequestRepository())
