from datetime import datetime

from pydantic import BaseModel


class BaseUser(BaseModel):
    name: str
    email: str


class User(BaseUser):
    active: bool
    creation_date: datetime
    last_login: datetime | None

    model_config = {"from_attributes": True}


class CreateUser(BaseUser):
    password: str
