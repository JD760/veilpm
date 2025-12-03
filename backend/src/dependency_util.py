from fastapi import Request
from uuid import UUID
from .models.user import User
from .security import TokenHandler
from .database.user import DbUser, get_user
from .settings import Settings
from sqlalchemy.orm import Session


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_user_from_token(
    settings: Settings,
    session: Session,
    token: str,
) -> User:
    handler = TokenHandler(settings)
    payload = handler.decode_or_http_error(token)
    user_id: UUID = UUID(payload["sub"])
    database_user: DbUser = get_user(session, user_id)
    return User.model_validate(database_user)
