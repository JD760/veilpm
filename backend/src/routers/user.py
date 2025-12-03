from datetime import datetime
from http import HTTPStatus
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dbutil import get_session
from src.dependency_util import get_settings
from src.database.user import DbUser, get_user_by_name, insert_user
from src.models.user import CreateUser, User
from src.security import PasswordHandler, TokenHandler
from src.settings import Settings

from .auth import oauth2_scheme

router = APIRouter(prefix="/users")
USERS_TAG = "User"


@router.get(
    "/me",
    name="Get current user",
    description="Get details of the user currently authenticated",
    response_model=User,
    tags=[USERS_TAG],
)
def get_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> User:
    token_handler = TokenHandler(settings)
    token_payload = token_handler.decode_or_http_error(token)
    user_name = token_payload.get("sub", None)
    user: DbUser = get_user_by_name(session, user_name)
    return User.model_validate(user)


@router.post(
    "/",
    name="Create a new user",
    description="Create a new user, if permitted to do so",
    tags=[USERS_TAG],
)
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
        id=uuid4(),
        name=body.name,
        email=body.email,
        active=True,
        creation_date=datetime.now(),
        password_hash=password_handler.hash(body.password),
    )
    insert_user(session, user)
    return HTTPStatus.OK
