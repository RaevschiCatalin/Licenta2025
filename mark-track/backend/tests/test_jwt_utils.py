import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from utils.jwt_utils import create_access_token, verify_token

def test_create_access_token():
    """Test JWT token creation."""
    data = {"sub": "test@example.com", "role": "user"}
    token = create_access_token(data)
    
    # Token should be a string
    assert isinstance(token, str)
    assert len(token) > 0

def test_verify_token():
    """Test JWT token verification."""
    data = {"sub": "test@example.com", "role": "user"}
    token = create_access_token(data)
    
    # Verify the token
    payload = verify_token(token)
    
    # Check payload contents
    assert payload["sub"] == data["sub"]
    assert payload["role"] == data["role"]
    assert "exp" in payload

def test_token_expiration():
    """Test that tokens expire correctly."""
    data = {"sub": "test@example.com"}
    # Create token with 1 second expiration
    token = create_access_token(data, expires_delta=timedelta(seconds=1))
    
    # Token should be valid initially
    payload = verify_token(token)
    assert payload["sub"] == data["sub"]
    
    # Wait for token to expire
    import time
    time.sleep(2)
    
    # Token should be invalid after expiration
    with pytest.raises(HTTPException) as exc_info:
        verify_token(token)
    assert exc_info.value.status_code == 401

def test_invalid_token():
    """Test handling of invalid tokens."""
    # Test with malformed token
    with pytest.raises(HTTPException) as exc_info:
        verify_token("invalid.token.here")
    assert exc_info.value.status_code == 401
    
    # Test with empty token
    with pytest.raises(HTTPException) as exc_info:
        verify_token("")
    assert exc_info.value.status_code == 401

def test_token_with_custom_expiration():
    """Test token creation with custom expiration."""
    data = {"sub": "test@example.com"}
    # Create token with 5 minutes expiration
    token = create_access_token(data, expires_delta=timedelta(minutes=5))
    
    payload = verify_token(token)
    exp_time = datetime.fromtimestamp(payload["exp"])
    now = datetime.utcnow()
    
    # Check that expiration is roughly 5 minutes from now
    time_diff = exp_time - now
    assert timedelta(minutes=4, seconds=55) <= time_diff <= timedelta(minutes=5, seconds=5) 