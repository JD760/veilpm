from datetime import datetime
from src.core.repositories.crud_repository import CrudRepository
from uuid import UUID
from .models import DbUser


class UserRepository(CrudRepository):
    def __init__(self, session):
        super().__init__(session, DbUser)
        self.session = session

    def get_user_by_name(self, user_name: str) -> list[DbUser]:
        return self.get_by_field("name", user_name)

    def set_last_login(self, user_id: UUID):
        user: DbUser = self.get_by_id(user_id)
        self.session.delete(user)
        user.last_login = datetime.now()
        self.create(user)
