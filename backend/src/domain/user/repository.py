from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.core.security import TokenHandler
from uuid import UUID
from .models import DbUser
from .schema import User


class RequestRepository:
    def get_user(self, session: Session, user_id: UUID) -> DbUser:
        return self._Queries.get_user_by_id(session, user_id)

    def get_user_by_name(self, session: Session, user_name: str) -> DbUser:
        return self._Queries.get_user_by_name(session, user_name)

    def insert_user(session: Session, user: DbUser):
        session.add(user)
        session.commit()
        session.refresh(user)

    def set_last_login(self, session: Session, user_id: UUID):
        user: DbUser = self._Queries.get_user_by_id(session, user_id)
        session.delete(user)
        user.last_login = datetime.now()
        session.add(user)
        session.commit()
        session.refresh(user)

    def get_user_from_token(
        self,
        session: Session,
        token: str,
    ) -> User:
        payload = TokenHandler.decode_or_http_error(token)
        user_id: UUID = UUID(payload["sub"])
        database_user: DbUser = self.get_user(session, user_id)
        return User.model_validate(database_user)

    class _Queries:
        @classmethod
        def get_user_by_id(cls, session: Session, user_id: UUID):
            return session.execute(
                select(DbUser).where(DbUser.id == user_id)
            ).scalar_one_or_none()

        @classmethod
        def get_user_by_name(cls, session: Session, user_name: str):
            # NOTE: This may fail in future if we support
            # multiple users with the same name
            return session.execute(
                select(DbUser).where(DbUser.name == user_name)
            ).scalar_one_or_none()
