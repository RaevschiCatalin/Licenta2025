# import pytest
from utils.security import verify_password, get_password_hash

def test_password_hashing():
    """Test that password hashing works correctly."""
    password = "test_password123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    
    assert verify_password(password, hashed)
    
    assert not verify_password("wrong_password", hashed)

def test_password_hash_uniqueness():
    """Test that same password produces different hashes."""
    password = "test_password123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    assert hash1 != hash2
    
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)

def test_password_verification_edge_cases():
    """Test password verification with edge cases."""
    password = "test_password123"
    hashed = get_password_hash(password)
    
    assert not verify_password("", hashed)
    
    long_password = "a" * 1000
    long_hashed = get_password_hash(long_password)
    assert verify_password(long_password, long_hashed)
    
    special_password = "!@#$%^&*()_+"
    special_hashed = get_password_hash(special_password)
    assert verify_password(special_password, special_hashed) 