from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Union
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from camera_collector.core.config import settings
from camera_collector.models.user import User
from camera_collector.core.exceptions import AuthenticationError


# Password hashing
# Use fewer rounds in test environment for speed
import os
bcrypt_rounds = int(os.environ.get("BCRYPT_ROUNDS", 12))

# Configure bcrypt with fewer rounds for testing
try:
    # Fix for bcrypt compatibility issues
    import bcrypt
    # Test if bcrypt is working correctly
    test_hash = bcrypt.hashpw(b"test", bcrypt.gensalt(rounds=4))
    # Use our tested bcrypt backend
    pwd_context = CryptContext(
        schemes=["bcrypt"], 
        deprecated="auto",
        bcrypt__rounds=bcrypt_rounds,
        bcrypt__ident="2b"
    )
except Exception as e:
    print(f"Warning: Using bcrypt without custom rounds due to compatibility issue: {e}")
    # Fallback to default settings
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash.
    
    Args:
        plain_password: The plaintext password
        hashed_password: The hashed password
        
    Returns:
        True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password.
    
    Args:
        password: The plaintext password
        
    Returns:
        The hashed password
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, int], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a new JWT access token.
    
    Args:
        subject: Token subject (typically user ID)
        expires_delta: Optional token expiration time
        
    Returns:
        JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(
    subject: Union[str, int], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a new JWT refresh token.
    
    Args:
        subject: Token subject (typically user ID)
        expires_delta: Optional token expiration time
        
    Returns:
        JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Get the current authenticated user from a JWT token.
    
    Args:
        token: JWT token
        
    Returns:
        User payload
        
    Raises:
        AuthenticationError: If token is invalid
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise AuthenticationError("Could not validate credentials")
        
        return {"id": user_id}
    except (JWTError, ValidationError):
        raise AuthenticationError("Could not validate credentials")