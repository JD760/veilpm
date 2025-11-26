from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class User(BaseModel):
    id: UUID
    name: str
    email: str
    active: bool
    creation_date: datetime
    last_login: datetime
