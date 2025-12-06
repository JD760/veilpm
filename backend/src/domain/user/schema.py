from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserID(BaseModel):
    user_id: UUID


class BaseUser(BaseModel):
    name: str
    email: str


class User(BaseUser):
    id: UUID
    active: bool
    creation_date: datetime
    last_login: datetime | None

    model_config = {"from_attributes": True}


class CreateUser(BaseUser):
    password: str
