import pytest
from fastapi.testclient import TestClient
import json

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

def test_csrf_protection(client, auth_headers):
    response = client.get("/csrf-token")
    assert response.status_code == 200
    csrf_token = response.json()["csrf_token"]
    
    headers = {**auth_headers, "X-CSRF-Token": csrf_token}
    response = client.post("/users/profile", json={}, headers=headers)
    assert response.status_code == 200
    
    headers = {**auth_headers, "X-CSRF-Token": "invalid_token"}
    response = client.post("/users/profile", json={}, headers=headers)
    assert response.status_code == 403
    
    response = client.post("/users/profile", json={}, headers=auth_headers)
    assert response.status_code == 403

def test_xss_prevention(client, auth_headers):
    xss_payloads = [
        "<script>alert('xss')</script>",
        "javascript:alert('xss')",
        "<img src=x onerror=alert('xss')>",
        "<svg/onload=alert('xss')>",
        "'-alert('xss')-'"
    ]
    
    for payload in xss_payloads:
        response = client.post(
            "/users/profile",
            json={"first_name": payload},
            headers=auth_headers
        )
        assert response.status_code == 200
        
        response = client.get("/users/profile", headers=auth_headers)
        assert response.status_code == 200
        assert payload not in response.text
        assert "&lt;" in response.text or "&gt;" in response.text

def test_sql_injection_prevention(client, auth_headers):
    sql_injection_payloads = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT * FROM users; --",
        "' OR 1=1; --",
        "admin' --"
    ]
    
    for payload in sql_injection_payloads:
        response = client.post(
            "/auth/login",
            json={
                "email": payload,
                "password": "password123"
            }
        )
        assert response.status_code in [400, 401]
        
        response = client.get(
            f"/users/search?q={payload}",
            headers=auth_headers
        )
        assert response.status_code in [200, 400]
        assert "error" not in response.text.lower()

def test_file_upload_security(client, auth_headers):
    malicious_files = [
        ("test.php", b"<?php echo 'malicious'; ?>"),
        ("test.exe", b"MZ..."),
        ("test.jpg", b"GIF89a<?php system('rm -rf /'); ?>"),
        ("test.pdf", b"%PDF-1.4\n<?php system('cat /etc/passwd'); ?>")
    ]
    
    for filename, content in malicious_files:
        files = {"file": (filename, content, "application/octet-stream")}
        response = client.post("/users/upload", files=files, headers=auth_headers)
        assert response.status_code == 400
        
    large_file = b"0" * (10 * 1024 * 1024 + 1)
    files = {"file": ("large.txt", large_file, "text/plain")}
    response = client.post("/users/upload", files=files, headers=auth_headers)
    assert response.status_code == 400
    
    valid_files = [
        ("test.jpg", b"fake image content", "image/jpeg"),
        ("test.png", b"fake image content", "image/png"),
        ("test.pdf", b"fake pdf content", "application/pdf")
    ]
    
    for filename, content, content_type in valid_files:
        files = {"file": (filename, content, content_type)}
        response = client.post("/users/upload", files=files, headers=auth_headers)
        assert response.status_code == 200 