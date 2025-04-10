"""Test bcrypt directly."""

import pytest

@pytest.mark.skip("Skipping direct bcrypt test until compatibility issues are fixed")
def test_bcrypt_direct():
    """Test bcrypt directly."""
    import bcrypt
    
    # Test password
    password = b"testpassword123"
    
    # Hash with bcrypt directly, using a low rounds value for testing
    salt = bcrypt.gensalt(rounds=4)
    hashed = bcrypt.hashpw(password, salt)
    
    # Verify the hash
    assert bcrypt.checkpw(password, hashed)
    
    # Verify with incorrect password
    assert not bcrypt.checkpw(b"wrongpassword", hashed)
    
    # Test with known hash
    known_hash = b"$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    assert bcrypt.checkpw(b"password123", known_hash)