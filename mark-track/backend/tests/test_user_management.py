import pytest
from fastapi.testclient import TestClient

@pytest.fixture(scope="function")
def client(db):
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def auth_headers(client):
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
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_user_profile_operations(client, auth_headers):
    profile_data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+1234567890",
        "address": "123 Main St"
    }
    
    response = client.post("/users/profile", json=profile_data, headers=auth_headers)
    assert response.status_code == 200
    
    response = client.get("/users/profile", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["first_name"] == profile_data["first_name"]
    
    update_data = {"first_name": "Jane", "phone": "+0987654321"}
    response = client.put("/users/profile", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    
    response = client.get("/users/profile", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["first_name"] == update_data["first_name"]
    assert response.json()["phone"] == update_data["phone"]
    
    response = client.delete("/users/profile", headers=auth_headers)
    assert response.status_code == 200
    
    response = client.get("/users/profile", headers=auth_headers)
    assert response.status_code == 404

def test_user_role_management(client, auth_headers):
    response = client.get("/users/roles", headers=auth_headers)
    assert response.status_code == 200
    initial_roles = response.json()["roles"]
    
    response = client.post(
        "/users/roles",
        json={"role": "editor"},
        headers=auth_headers
    )
    assert response.status_code == 200
    
    response = client.get("/users/roles", headers=auth_headers)
    assert response.status_code == 200
    assert "editor" in response.json()["roles"]
    
    response = client.delete(
        "/users/roles/editor",
        headers=auth_headers
    )
    assert response.status_code == 200
    
    response = client.get("/users/roles", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["roles"] == initial_roles

def test_user_preferences(client, auth_headers):
    preferences = {
        "theme": "dark",
        "language": "en",
        "notifications": {
            "email": True,
            "push": False
        }
    }
    
    response = client.post("/users/preferences", json=preferences, headers=auth_headers)
    assert response.status_code == 200
    
    response = client.get("/users/preferences", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["theme"] == preferences["theme"]
    
    update = {"theme": "light", "notifications": {"email": False}}
    response = client.put("/users/preferences", json=update, headers=auth_headers)
    assert response.status_code == 200
    
    response = client.get("/users/preferences", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["theme"] == update["theme"]
    assert response.json()["notifications"]["email"] == update["notifications"]["email"] 