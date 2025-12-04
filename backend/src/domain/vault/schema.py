from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class BaseVault(BaseModel):
    name: str
    description: str


class Vault(BaseVault):
    id: UUID
    owner: UUID
    creation_date: datetime
    model_config = {"from_attributes": True}


class CreateVault(BaseVault):
    passphrase: str
