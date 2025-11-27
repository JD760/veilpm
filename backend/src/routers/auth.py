from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dbutil import get_session, query_db_for_user
from src.models.auth import Token
from src.security import PasswordHandler, TokenHandler
from src.settings import Settings
from src.tables.user import DbUser
from src.dependency_util import get_settings

router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth", scheme_name="JWT")


@router.get("/")
def auth_check(
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings)
) -> dict[str, bool]:
    handler = TokenHandler(settings)
    return {"valid_session": handler.verify_or_http_error(token)}


@router.post("/", response_model=Token)
def create_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_session),
) -> Token:
    token_handler = TokenHandler(settings)
    password_handler = PasswordHandler(settings)
    user: DbUser = query_db_for_user(session, form_data.username)
    if not user.password_hash:
        raise HTTPException(HTTPStatus.FORBIDDEN, "User has not been set up")
    if not password_handler.verify(form_data.password, user.password_hash):
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Incorrect password")

    token: str = token_handler.encode(user.name)
    return Token(access_token=token, token_type="Bearer")
