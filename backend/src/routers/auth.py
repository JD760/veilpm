from dataclasses import dataclass
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated, Any
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Header, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt.api_jwt as jwt
from sqlalchemy.orm import Session
import os
from src.security import PasswordHandler, TokenHandler, query_db_for_user
from src.dbutil import get_session
from src.models.auth import Token
from src.models.user import User
from src.settings import Settings
from src.tables.user import DbUser

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth", scheme_name="JWT")

def get_settings(request: Request) -> Settings:
    return request.app.state.settings
    
def require_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)) -> User:
    print(f"Token provided: {token}")
    pass

fake_users = {
    "admin": {"user_name": "admin", "password": "password"},
    "jd4": {"user_name": "jd4", "password": "test"},
}



def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings = Depends(get_settings),
) -> dict[str, str]:
    try:
        payload = jwt.decode(
            token, key=settings.jwt_secret_key, algorithms=settings.jwt_algorithm
        )
    except:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"user": payload["sub"]}

@router.get("/auth")
def auth_check(token: str, settings: Settings = Depends(get_settings)) -> dict[str, bool]:
    handler = TokenHandler(settings)
    return {"valid_session": handler.verify_or_http_error(token)}


@router.get("/users/me")
def get_user(current_user: Annotated[dict[str, str], Depends(require_user)]):
    print(f"Current user: {current_user}")
    return current_user


@router.post("/auth", response_model=Token)
def create_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_session)
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

