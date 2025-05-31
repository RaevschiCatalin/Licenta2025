# import pytest
from utils.security import verify_password, get_password_hash

def test_password_hashing():
    """Test that password hashing works correctly."""
    password = "test_password123"
    hashed = get_password_hash(password)
    
    # Verify the hash is different from the original password
    assert hashed != password
    
    # Verify the hash can be verified
    assert verify_password(password, hashed)
    
    # Verify wrong password fails
    assert not verify_password("wrong_password", hashed)

def test_password_hash_uniqueness():
    """Test that same password produces different hashes."""
    password = "test_password123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    # Hashes should be different due to salt
    assert hash1 != hash2
    
    # But both should verify correctly
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)

def test_password_verification_edge_cases():
    """Test password verification with edge cases."""
    password = "test_password123"
    hashed = get_password_hash(password)
    
    # Test empty password
    assert not verify_password("", hashed)
    
    # Test very long password
    long_password = "a" * 1000
    long_hashed = get_password_hash(long_password)
    assert verify_password(long_password, long_hashed)
    
    # Test special characters
    special_password = "!@#$%^&*()_+"
    special_hashed = get_password_hash(special_password)
    assert verify_password(special_password, special_hashed) 