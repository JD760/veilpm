from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from src.core.security import TokenHandler, PasswordHandler, oauth2_scheme
from uuid import uuid4
from datetime import datetime
from src.core.db import get_session
from src.core.config import settings
from .schema import User, CreateUser
from .models import DbUser
from src.core.config import logger
from .service import get_user_service
from src.interfaces.db_session import DBSession

router = APIRouter(prefix="/users")
USERS_TAG = "Users"


@router.get(
    "/me",
    name="Get current user",
    description="Get details of the user currently authenticated",
    response_model=User,
    tags=[USERS_TAG],
)
def get_user(
    token: str = Depends(oauth2_scheme),
    session: DBSession = Depends(get_session),
    user_service=Depends(get_user_service),
) -> User:
    token_payload = TokenHandler.decode_or_http_error(token)
    user_name = token_payload.get("sub", None)
    logger.critical(f"User: {user_name}")
    user: DbUser = user_service.get_user(session, user_name)
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
    user_service=Depends(get_user_service),
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
    user_service.insert_user(user)
    return HTTPStatus.OK
