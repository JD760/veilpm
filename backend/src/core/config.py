from pydantic import SecretStr
from pydantic_settings import BaseSettings
from logging import Logger


class Settings(BaseSettings):
    postgres_port: int
    postgres_user: str
    postgres_password: SecretStr
    database_host: str
    database_port: int
    database_name: str

    jwt_secret_key: SecretStr
    jwt_algorithm: str
    jwt_session_timeout: int = 60 * 24

    debug: bool


logger = Logger("Logger")
settings = Settings()
