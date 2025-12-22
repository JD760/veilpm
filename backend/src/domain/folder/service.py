from uuid import UUID
from src.core.db import Queries
from src.domain.vault.models import DbVaultFolder
from src.domain.vault.schema import VaultFolder
from .repository import RequestRepository
from .schema import Folder


class FolderService:
    def __init__(self, repository):
        self._repository: RequestRepository = repository

    def get_vault_folders(self, session, vault_id: UUID) -> list[Folder]:
        rows: list[DbVaultFolder] = Queries.get_by_field(
            session,
            DbVaultFolder,
            "vault_id",
            vault_id,
        )
        vault_folders = [VaultFolder.model_validate(row) for row in rows]
        return vault_folders


folder_service = FolderService(RequestRepository())
