from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.dbutil import get_session
from src.database.user import get_user_by_name, set_last_login
from src.dependency_util import get_settings
from src.models.auth import Token
from src.database.user import DbUser
from src.security import PasswordHandler, TokenHandler
from src.settings import Settings

router = APIRouter(prefix="/auth")
AUTH_TAG = "Authentication"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", scheme_name="JWT")


@router.get("/status", tags=[AUTH_TAG])
def auth_check(
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    handler = TokenHandler(settings)
    return {"valid_session": handler.verify_or_http_error(token)}


@router.post("/token", response_model=Token, tags=[AUTH_TAG])
def create_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_session),
) -> Token:
    token_handler = TokenHandler(settings)
    password_handler = PasswordHandler(settings)
    user: DbUser = get_user_by_name(session, form_data.username)
    if not password_handler.verify(form_data.password, user.password_hash):
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Incorrect password")

    set_last_login(session, user.id)
    token: str = token_handler.encode(user.id)
    return Token(access_token=token, token_type="Bearer")
