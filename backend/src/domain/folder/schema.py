from uuid import UUID
from pydantic import BaseModel


class Folder(BaseModel):
    id: UUID
    owner: UUID
    parent_folder: UUID
    name: str
