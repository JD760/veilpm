from typing import Optional
from urllib.parse import quote

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from .settings import Settings

engine: Optional[Engine] = None
sessionLocal: Optional[sessionmaker] = None


def init_database(settings):
    # This should be evil but is actually recommended
    # for handling a session factory
    global engine, sessionLocal
    engine = create_engine(get_connection_uri(settings))
    sessionLocal = sessionmaker(bind=engine)


def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_connection_uri(settings: Settings):
    return f"""postgresql+psycopg
        ://{settings.postgres_user}
        :{quote(settings.postgres_password.get_secret_value())}
        @{settings.database_host}
        /{settings.database_name}
    """
