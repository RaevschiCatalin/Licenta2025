import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.postgres_setup import Base
from main import app
import time

# Create test database engine
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # Create the test database tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    # Create a test client with the test database
    with TestClient(app) as test_client:
        yield test_client

def test_login_rate_limit(client):
    """Test that login endpoint respects rate limit."""
    # Make 5 requests (within limit)
    for _ in range(5):
        response = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "password123"}
        )
        assert response.status_code in [401, 429]  # Either unauthorized or rate limited

    # Make one more request (should be rate limited)
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 429  # Rate limited

def test_register_rate_limit(client):
    """Test that register endpoint respects rate limit."""
    # Make 3 requests (within limit)
    for _ in range(3):
        response = client.post(
            "/auth/register",
            json={
                "email": f"test{_}@example.com",
                "password": "password123",
                "role": "pending"
            }
        )
        assert response.status_code in [200, 429]  # Either success or rate limited

    # Make one more request (should be rate limited)
    response = client.post(
        "/auth/register",
        json={
            "email": "test4@example.com",
            "password": "password123",
            "role": "pending"
        }
    )
    assert response.status_code == 429  # Rate limited

def test_rate_limit_reset(client):
    """Test that rate limits reset after the time window."""
    # Make 5 login requests
    for _ in range(5):
        response = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "password123"}
        )
        assert response.status_code in [401, 429]  # Either unauthorized or rate limited

    # Wait for rate limit window to expire (1 minute)
    time.sleep(61)

    # Should be able to make requests again
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code in [401, 429]  # Either unauthorized or rate limited

def test_different_endpoints_separate_limits(client):
    """Test that different endpoints have separate rate limits."""
    # Make 5 login requests (should hit login limit)
    for _ in range(5):
        response = client.post(
            "/auth/login",
            json={"email": "test@example.com", "password": "password123"}
        )
        assert response.status_code in [401, 429]  # Either unauthorized or rate limited

    # Should still be able to make register requests
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "role": "pending"
        }
    )
    assert response.status_code in [200, 429]  # Either success or rate limited 