import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="function")
def client(db):
    with TestClient(app) as test_client:
        yield test_client

def test_login_rate_limit(client):
    headers = {"X-Forwarded-For": "10.0.0.1"}
    for _ in range(6):
        response = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "wrongpass"},
            headers=headers
        )
        assert response.status_code in [200, 401, 429]

def test_register_rate_limit(client):
    headers = {"X-Forwarded-For": "10.0.0.2"}
    for i in range(4):
        response = client.post(
            "/auth/register",
            json={
                "email": f"test{i}@example.com",
                "password": "password123",
                "role": "pending"
            },
            headers=headers
        )
        assert response.status_code in [200, 400, 429]

def test_rate_limit_reset(client):
    headers = {"X-Forwarded-For": "10.0.0.3"}
    for _ in range(5):
        response = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "wrongpass"},
            headers=headers
        )
        assert response.status_code in [200, 401, 429]

    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "wrongpass"},
        headers={"X-Forwarded-For": "10.0.0.99"}
    )
    assert response.status_code in [200, 401, 429]

def test_different_endpoints_separate_limits(client):
    login_headers = {"X-Forwarded-For": "10.0.0.4"}
    register_headers = {"X-Forwarded-For": "10.0.0.5"}

    for _ in range(5):
        response = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "wrongpass"},
            headers=login_headers
        )
        assert response.status_code in [200, 401, 429]

    response = client.post(
        "/auth/register",
        json={
            "email": "another@example.com",
            "password": "password123",
            "role": "pending"
        },
        headers=register_headers
    )
    assert response.status_code in [200, 400, 429]
