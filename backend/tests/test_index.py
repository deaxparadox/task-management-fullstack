from starlette.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_index():
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Everyone"}