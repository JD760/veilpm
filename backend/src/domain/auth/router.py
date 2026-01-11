from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.core.config import Settings
from src.core.dependencies import get_settings
from src.core.security import oauth2_scheme, TokenHandler, PasswordHandler
from src.domain.user.service import UserService, get_user_service
from src.domain.user.models import DbUser
from .schema import Token

router = APIRouter(prefix="/auth")
AUTH_TAG = "Auth"


@router.get("/status", tags=[AUTH_TAG])
def auth_check(
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    return {"valid_session": TokenHandler.verify_or_http_error(token)}


@router.post("/token", response_model=Token, tags=[AUTH_TAG])
def create_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service),
) -> Token:
    user: DbUser = user_service.get_user_by_name(form_data.username)
    if not PasswordHandler.verify(form_data.password, user.password_hash):
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Incorrect password")
    user_service.set_last_login(user.id)
    token: str = TokenHandler.encode(user.id)
    return Token(access_token=token, token_type="Bearer")
