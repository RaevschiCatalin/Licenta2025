import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import re

@pytest.fixture(scope="function")
def client(db):
    with TestClient(app) as test_client:
        yield test_client

def test_user_registration_validation(client):
    invalid_emails = [
        "invalid-email",
        "missing@domain",
        "@missing-local.com",
        "spaces in@email.com",
        "special@chars!.com"
    ]
    
    for email in invalid_emails:
        response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "password123",
                "role": "pending"
            }
        )
        assert response.status_code == 400

    weak_passwords = [
        "short",
        "onlylowercase",
        "ONLYUPPERCASE",
        "12345678",
        "no_numbers"
    ]
    
    for password in weak_passwords:
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": password,
                "role": "pending"
            }
        )
        assert response.status_code == 400

    invalid_roles = ["invalid_role", "admin", "superuser"]
    for role in invalid_roles:
        response = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "password": "StrongPass123!",
                "role": role
            }
        )
        assert response.status_code == 400

def test_user_activation_flow(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "StrongPass123!",
            "role": "pending"
        }
    )
    assert response.status_code == 200
    activation_token = response.json()["activation_token"]

    response = client.post(
        f"/auth/activate/{activation_token}"
    )
    assert response.status_code == 200

    response = client.post(
        f"/auth/activate/{activation_token}"
    )
    assert response.status_code == 400

    response = client.post(
        "/auth/activate/invalid_token"
    )
    assert response.status_code == 400

def test_password_reset_flow(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "StrongPass123!",
            "role": "pending"
        }
    )
    assert response.status_code == 200

    response = client.post(
        "/auth/request-password-reset",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 200
    reset_token = response.json()["reset_token"]

    response = client.post(
        "/auth/reset-password",
        json={
            "token": reset_token,
            "new_password": "NewStrongPass123!"
        }
    )
    assert response.status_code == 200

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "NewStrongPass123!"
        }
    )
    assert response.status_code == 200

def test_session_management(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "StrongPass123!",
            "role": "pending"
        }
    )
    assert response.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "StrongPass123!"
        }
    )
    assert login_response.status_code == 200
    session_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {session_token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200

    response = client.post("/auth/logout", headers=headers)
    assert response.status_code == 200

    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401 