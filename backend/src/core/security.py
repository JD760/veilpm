from datetime import datetime, timedelta
from functools import wraps
from uuid import UUID

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import api_jwt
from pwdlib import PasswordHash
from src.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", scheme_name="JWT")


class TokenHandler:
    jwt_secret_key = settings.jwt_secret_key.get_secret_value()
    jwt_algorithm = settings.jwt_algorithm
    jwt_session_timeout = settings.jwt_session_timeout

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

    @classmethod
    def encode(cls, user_id: UUID) -> str:
        expiry = datetime.now() + timedelta(minutes=cls.jwt_session_timeout)
        token_payload = {
            "sub": str(user_id),
            "exp": expiry,
        }

        return api_jwt.encode(
            token_payload,
            key=cls.jwt_secret_key,
            algorithm=cls.jwt_algorithm,
        )

    @classmethod
    def decode(cls, token: str) -> str:
        token_payload = api_jwt.decode(
            token, key=cls.jwt_secret_key, algorithms=cls.jwt_algorithm
        )
        return token_payload

    @classmethod
    @http_error_translator
    def decode_or_http_error(cls, token: str) -> str:
        return cls.decode(token)

    @classmethod
    def verify(cls, token: str) -> bool:
        return cls.decode(token) is not None

    @classmethod
    @http_error_translator
    def verify_or_http_error(cls, token: str) -> str:
        return cls.verify(token)


class PasswordHandler:
    algorithm: PasswordHash = PasswordHash.recommended()

    @classmethod
    def hash(cls, password: str):
        return cls.algorithm.hash(password)

    @classmethod
    def verify(cls, password: str, password_hash: str):
        return cls.algorithm.verify(password, password_hash)
