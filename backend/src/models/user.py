from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    name: str
    email: str
    active: bool
    creation_date: datetime
    last_login: datetime
