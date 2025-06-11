import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from utils.jwt_utils import create_access_token, verify_token

def test_create_access_token():
    data = {"sub": "test@example.com", "role": "user"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0

def test_verify_token():
    data = {"sub": "test@example.com", "role": "user"}
    token = create_access_token(data)
    
    payload = verify_token(token)
    
    assert payload["sub"] == data["sub"]
    assert payload["role"] == data["role"]
    assert "exp" in payload

def test_token_expiration():
    data = {"sub": "test@example.com"}
    token = create_access_token(data, expires_delta=timedelta(seconds=1))
    
    payload = verify_token(token)
    assert payload["sub"] == data["sub"]
    
    import time
    time.sleep(2)
    
    with pytest.raises(HTTPException) as exc_info:
        verify_token(token)
    assert exc_info.value.status_code == 401

def test_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        verify_token("invalid.token.here")
    assert exc_info.value.status_code == 401
    
    with pytest.raises(HTTPException) as exc_info:
        verify_token("")
    assert exc_info.value.status_code == 401

def test_token_with_custom_expiration():
    data = {"sub": "test@example.com"}
    token = create_access_token(data, expires_delta=timedelta(minutes=5))
    
    payload = verify_token(token)
    exp_time = datetime.fromtimestamp(payload["exp"])
    now = datetime.utcnow()
    
    time_diff = exp_time - now
    assert timedelta(minutes=4, seconds=55) <= time_diff <= timedelta(minutes=5, seconds=5) 