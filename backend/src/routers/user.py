from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dbutil import get_session, insert_user, query_db_for_user
from src.dependency_util import get_settings
from src.models.tables import DbUser
from src.models.user import CreateUser, User
from src.security import PasswordHandler, TokenHandler
from src.settings import Settings

from .auth import oauth2_scheme

router = APIRouter(prefix="/users")


@router.get("/me", response_model=User)
def get_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> User:
    token_handler = TokenHandler(settings)
    token_payload = token_handler.decode_or_http_error(token)
    user_name = token_payload.get("sub", None)
    user: DbUser = query_db_for_user(session, user_name)
    return User.model_validate(user)


@router.post("/")
def create_user(
    body: CreateUser,
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
):
    token_handler = TokenHandler(settings)
    token_payload = token_handler.decode_or_http_error(token)
    # TODO: We of course need a proper role and permission system
    if token_payload.get("sub") != "admin":
        raise HTTPException(
            HTTPStatus.UNAUTHORIZED, "Only administrators may create users"
        )

    password_handler = PasswordHandler(settings)
    user = DbUser(
        name=body.name,
        email=body.email,
        active=True,
        creation_date=datetime.now(),
        password_hash=password_handler.hash(body.password),
    )
    insert_user(session, user)
    return HTTPStatus.OK
