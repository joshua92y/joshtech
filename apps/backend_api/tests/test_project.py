from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_projects():
    response = client.get("/projects")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("title" in project for project in data)
