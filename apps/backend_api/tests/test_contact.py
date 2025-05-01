from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_submit_contact():
    response = client.post(
        "/contact",
        json={
            "name": "테스트 사용자",
            "email": "test@example.com",
            "message": "테스트 메시지입니다.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "테스트 사용자"
    assert data["email"] == "test@example.com"
    assert data["message"] == "테스트 메시지입니다."
