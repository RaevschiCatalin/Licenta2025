import pytest
from fastapi.testclient import TestClient
from main import app
from database.postgres_setup import SessionLocal
from models.database_models import User
import uuid

client = TestClient(app)

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_insecure_registration(db):
    # Test with extremely weak password
    response = client.post("/auth/register", params={
        "email": "test@example.com",
        "password": "123"  # Very weak password
    })
    assert response.status_code == 200
    
    # Password is stored in plaintext
    user = db.query(User).filter(User.email == "test@example.com").first()
    assert user.password == "123"

def test_sql_injection(db):
    # SQL injection attempt
    response = client.post("/auth/login", params={
        "email": "' OR '1'='1",
        "password": "' OR '1'='1"
    })
    # This should fail but demonstrates vulnerability
    assert response.status_code == 404

def test_password_exposure():
    # Register a user
    client.post("/auth/register", params={
        "email": "victim@example.com",
        "password": "secret123"
    })
    
    # Get all users and their passwords
    response = client.get("/auth/users")
    assert response.status_code == 200
    
    # We can see everyone's passwords
    users = response.json()
    assert any(user["password"] == "secret123" for user in users)

def test_brute_force():
    # No rate limiting, can try unlimited times
    for i in range(100):  # Try 100 times
        response = client.post("/auth/login", params={
            "email": "test@example.com",
            "password": f"guess{i}"
        })
        # No lockout after failed attempts
        assert response.status_code in [200, 401] 