import pytest
from app.schemas.user import UserCreate

def test_register_and_login(client):
    payload = {"username": "testuser", "email": "test@example.com", "password": "password123", "is_admin": True}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["is_admin"] == True

    login_payload = {"username": "testuser", "password": "password123"}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_refresh_token(client):

    payload = {"username": "user2", "email": "user2@example.com", "password": "123456", "is_admin": False}
    client.post("/auth/register", json=payload)
    login_payload = {"username": "user2", "password": "123456"}
    response = client.post("/auth/login", json=login_payload)
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/auth/refresh-token", headers=headers)
    assert response.status_code == 200
    new_token_data = response.json()
    assert "access_token" in new_token_data
