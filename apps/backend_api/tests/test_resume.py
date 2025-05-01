from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_resume():
    response = client.get("/resume")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "email" in data
