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

def test_register_user(db):
    # Test data
    test_uid = str(uuid.uuid4())
    test_email = "test@example.com"
    
    # Make request
    response = client.post("/auth/register", json={
        "uid": test_uid,
        "email": test_email
    })
    
    # Check response
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully in Firestore."
    
    # Check database
    user = db.query(User).filter(User.id == test_uid).first()
    assert user is not None
    assert user.email == test_email
    assert user.role == "pending"

def test_register_duplicate_user(db):
    # Test data
    test_uid = str(uuid.uuid4())
    test_email = "duplicate@example.com"
    
    # Create first user
    client.post("/auth/register", json={
        "uid": test_uid,
        "email": test_email
    })
    
    # Try to create duplicate
    response = client.post("/auth/register", json={
        "uid": test_uid,
        "email": test_email
    })
    
    # Check response
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"] 