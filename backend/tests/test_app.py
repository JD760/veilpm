from fastapi.testclient import TestClient


class TestApp:
    def test_healthcheck(self, test_client: TestClient):
        response = test_client.get("/")
        assert response is not None
        assert response.json() == {"status": "The service is up"}
