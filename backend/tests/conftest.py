from datetime import datetime
from uuid import uuid4
from fastapi.testclient import TestClient
import pytest
from src.domain.user.schema import User
from src.domain.vault.schema import Vault
from src.main import create_app

USER_1 = User(
    id=uuid4(),
    name="admin",
    email="test@mail.com",
    active=True,
    creation_date=datetime.now(),
    last_login=datetime.now(),
)

VAULT_1 = Vault(
    name="A test vault",
    description="Vault created for testing",
    id=uuid4(),
    owner=USER_1.id,
    creation_date=datetime.now(),
)


@pytest.fixture()
def test_client():
    app = create_app(test=True)
    return TestClient(app)
