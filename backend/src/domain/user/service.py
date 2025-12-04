from sqlalchemy import UUID
from .repository import RequestRepository
from .models import DbUser


class UserService:
    def __init__(self, repository):
        # FIXME Poor practice (saves on boilerplate for now)
        # should have a repo template
        self.repository: RequestRepository = repository

    def get_user_by_name(self, session, user_name: str) -> DbUser:
        return self.repository.get_user_by_name(session, user_name)

    def insert_user(self, session, user: DbUser):
        return self.repository.insert_user(session, user)

    def set_last_login(self, session, user_id: UUID):
        return self.repository.set_last_login(session, user_id)


user_service = UserService(RequestRepository())
