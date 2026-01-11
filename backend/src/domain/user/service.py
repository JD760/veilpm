from sqlalchemy import UUID
from src.core.db import get_session
from fastapi import Depends
from src.core.security import TokenHandler
from .repository import UserRepository
from .models import DbUser
from .schema import User


def get_user_service(session=Depends(get_session)):
    return UserService(session)


class UserService:
    def __init__(self, session):
        self.session = session
        self._repository = UserRepository(session)

    def get_user(self, user_id: UUID) -> DbUser:
        return self._repository.get_by_id(user_id)

    def get_user_by_name(self, user_name: str) -> DbUser:
        user = self._repository.get_user_by_name(user_name)
        if len(user) != 1:
            raise RuntimeError("User does not exist")
        return user[0]

    def insert_user(self, user: DbUser):
        return self._repository.create(user)

    def set_last_login(self, user_id: UUID):
        return self._repository.set_last_login(user_id)

    def get_user_from_token(self, token: str) -> User:
        payload = TokenHandler.decode_or_http_error(token)
        user_id: UUID = UUID(payload["sub"])
        database_user: DbUser = self.get_user(user_id)
        return User.model_validate(database_user)
