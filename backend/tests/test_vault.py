from fastapi import HTTPException
from .conftest import VAULT_1
import pytest


class TestVault:
    def test_check_ownership_fails(self):
        with pytest.raises(VAULT_1.check_ownership("non-existent-user")) as e:
            assert e.errisinstance(HTTPException)

    def test_check_ownership(self):
        assert VAULT_1.check_ownership(VAULT_1.owner)
