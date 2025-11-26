from dataclasses import dataclass
from functools import wraps
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from jwt import api_jwt
from pwdlib import PasswordHash
from src.settings import Settings
from .tables.user import DbUser
from datetime import datetime, timedelta


class TokenHandler:
    def __init__(self, settings: Settings):
        self.jwt_secret_key = settings.jwt_secret_key.get_secret_value()
        self.jwt_algorithm = settings.jwt_algorithm
        self.jwt_session_timeout = settings.jwt_session_timeout
        
    @staticmethod
    def http_error_translator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except api_jwt.ExpiredSignatureError:
                return HTTPException(401, "Expired Token")
            except api_jwt.DecodeError:
                return HTTPException(400, "Malformed Token")
        return wrapper
    
    def encode(self, user_name: str) -> str:
        token_payload = {
            "sub": user_name,
            "exp": datetime.now() + timedelta(minutes=self.jwt_session_timeout),
        }
        
        return api_jwt.encode(
            token_payload,
            key=self.jwt_secret_key,
            algorithm=self.jwt_algorithm
        )
        
    def decode(self, token: str) -> str:
        token_payload = api_jwt.decode(
            token,
            key=self.jwt_secret_key,
            algorithms=self.jwt_algorithm
        )
        return token_payload
    
    @http_error_translator
    def decode_or_http_error(self, token: str) -> str:
        return self.decode(token)
    
    def verify(self, token: str) -> bool:
        return self.decode(token) is not None
    
    @http_error_translator
    def verify_or_http_error(self, token: str) -> str:
        return self.verify(token)
    
class PasswordHandler:
    def __init__(self, settings: Settings):
        self.password_hash: PasswordHash = PasswordHash.recommended()
    
    def hash(self, password: str):
        return self.password_hash.hash(password)
    
    def verify(self, password: str, password_hash: str):
        return self.password_hash.verify(password, password_hash)


def query_db_for_user(session: Session, user_name: str) -> DbUser:
    return session.execute(
        select(DbUser)
        .where(DbUser.name == user_name)
    ).scalar_one_or_none()
    