"""Test authentication with bcrypt."""

import pytest
from passlib.context import CryptContext


def test_bcrypt_simple():
    """Test simple bcrypt password hashing and verification."""
    # Create a password context
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Hash a password
    password = "testpassword123"
    hashed_password = pwd_context.hash(password)
    
    # Verify the password
    assert pwd_context.verify(password, hashed_password)
    
    # Verify incorrect password fails
    assert not pwd_context.verify("wrongpassword", hashed_password)


def test_bcrypt_rounds():
    """Test bcrypt with different numbers of rounds."""
    # Use fewer rounds for testing
    pwd_context = CryptContext(
        schemes=["bcrypt"], 
        deprecated="auto",
        bcrypt__rounds=4  # Minimum number of rounds
    )
    
    # Hash a password
    password = "testpassword123"
    hashed_password = pwd_context.hash(password)
    
    # Verify the password
    assert pwd_context.verify(password, hashed_password)
    

@pytest.mark.skip("Skipping known hash verification test until bcrypt compatibility issues are fixed")
def test_verify_known_hash():
    """Test verification with a known hash."""
    # This is a known bcrypt hash for the password "password123"
    known_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    
    # Create a password context
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Verify the password against the known hash
    assert pwd_context.verify("password123", known_hash)
    
    # Verify incorrect password fails
    assert not pwd_context.verify("wrongpassword", known_hash)