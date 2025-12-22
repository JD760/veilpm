from datetime import datetime
from http import HTTPStatus
from uuid import UUID
from fastapi import HTTPException
from pydantic import BaseModel


class BaseVault(BaseModel):
    name: str
    description: str


class Vault(BaseVault):
    id: UUID
    owner: UUID
    creation_date: datetime
    model_config = {"from_attributes": True}

    def check_ownership(self, user_id: str):
        if self.owner != user_id:
            raise HTTPException(
                HTTPStatus.UNAUTHORIZED,
                "Not authorised to access vault",
            )


class CreateVault(BaseVault):
    passphrase: str


class VaultUser(BaseModel):
    user_id: UUID
    vault_id: UUID
    model_config = {"from_attributes": True}


class VaultFolder(BaseModel):
    folder_id: UUID
    vault_id: UUID
    model_config = {"from_attributes": True}
