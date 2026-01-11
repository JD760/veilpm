from uuid import UUID
from src.core.db import Queries, get_session
from fastapi import Depends
from src.domain.vault.models import DbVaultFolder
from src.domain.vault.schema import VaultFolder
from .repository import FolderRepository
from .schema import Folder


def get_folder_service(session=Depends(get_session)):
    return FolderService(session)


class FolderService:
    def __init__(self, session):
        self._repository = FolderRepository(session)

    def get_vault_folders(self, session, vault_id: UUID) -> list[Folder]:
        rows: list[DbVaultFolder] = Queries.get_by_field(
            session,
            DbVaultFolder,
            "vault_id",
            vault_id,
        )
        vault_folders = [VaultFolder.model_validate(row) for row in rows]
        return vault_folders
