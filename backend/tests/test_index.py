from starlette.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_index():
    response = client.get("/api")
    print(f"\n\n{response}")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Everyone"}