from sqlalchemy import UUID
from .repository import RequestRepository
from .models import DbUser
from .schema import User


class UserService:
    def __init__(self, repository):
        # FIXME Poor practice (saves on boilerplate for now)
        # should have a repo template
        self._repository: RequestRepository = repository

    def get_user(self, session, user_id: UUID) -> DbUser:
        return self._repository.get_user(session, user_id)

    def get_user_by_name(self, session, user_name: str) -> DbUser:
        return self._repository.get_user_by_name(session, user_name)

    def insert_user(self, session, user: DbUser):
        return self._repository.insert_user(session, user)

    def set_last_login(self, session, user_id: UUID):
        return self._repository.set_last_login(session, user_id)

    def get_user_from_token(self, session, token: str) -> User:
        return self._repository.get_user_from_token(session, token)


user_service = UserService(RequestRepository())
