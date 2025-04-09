import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import time
from unittest.mock import patch, AsyncMock, MagicMock

from camera_collector.core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user
)
from camera_collector.core.config import settings
from camera_collector.core.exceptions import AuthenticationError


class TestSecurity:
    """Test security utilities."""
    
    @patch('camera_collector.core.security.pwd_context')
    def test_password_hashing(self, mock_pwd_context):
        """Test password hashing and verification with mocks."""
        from camera_collector.core.security import verify_password, get_password_hash
        
        # Setup the mock
        password = "test_password"
        hashed_password = "hashed_password_value"
        mock_pwd_context.hash.return_value = hashed_password
        mock_pwd_context.verify.return_value = True
        
        # Call the function
        result = get_password_hash(password)
        
        # Check the result
        assert result == hashed_password
        mock_pwd_context.hash.assert_called_once_with(password)
        
        # Test verify password
        verify_result = verify_password(password, hashed_password)
        assert verify_result is True
        mock_pwd_context.verify.assert_called_once_with(password, hashed_password)
    
    def test_create_access_token(self):
        """Test creating access tokens."""
        # Create a token
        user_id = "123"
        token = create_access_token(user_id)
        
        # Decode and verify the token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        assert payload["sub"] == user_id
        assert "exp" in payload
    
    def test_create_access_token_with_expiry(self):
        """Test creating access tokens with custom expiry."""
        # Create a token with a short expiry
        user_id = "123"
        expires_delta = timedelta(minutes=5)
        token = create_access_token(user_id, expires_delta=expires_delta)
        
        # Decode and verify the token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        assert payload["sub"] == user_id
        assert "exp" in payload
        
        # Since we can't reliably test the exact expiration time in a unit test,
        # just verify that the expiration time is in the future
        current_timestamp = int(time.time())
        assert payload["exp"] > current_timestamp
    
    def test_create_refresh_token(self):
        """Test creating refresh tokens."""
        # Create a token
        user_id = "123"
        token = create_refresh_token(user_id)
        
        # Decode and verify the token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        assert payload["sub"] == user_id
        assert "exp" in payload
    
    def test_create_refresh_token_with_expiry(self):
        """Test creating refresh tokens with custom expiry."""
        # Create a token with a short expiry
        user_id = "123"
        expires_delta = timedelta(hours=1)
        token = create_refresh_token(user_id, expires_delta=expires_delta)
        
        # Decode and verify the token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        assert payload["sub"] == user_id
        assert "exp" in payload
        
        # Since we can't reliably test the exact expiration time in a unit test,
        # just verify that the expiration time is in the future
        current_timestamp = int(time.time())
        assert payload["exp"] > current_timestamp
    
    @pytest.mark.asyncio
    @patch('camera_collector.core.security.jwt.decode')
    async def test_get_current_user_valid(self, mock_jwt_decode):
        """Test get_current_user with valid token."""
        # Mock JWT decode to return a valid payload
        user_id = "test_user_id"
        mock_jwt_decode.return_value = {"sub": user_id}
        
        # Call the function
        result = await get_current_user("valid_token")
        
        # Check the result
        assert result == {"id": user_id}
        mock_jwt_decode.assert_called_once_with(
            "valid_token", settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    
    @pytest.mark.asyncio
    @patch('camera_collector.core.security.jwt.decode')
    async def test_get_current_user_missing_sub(self, mock_jwt_decode):
        """Test get_current_user with missing sub claim."""
        # Mock JWT decode to return a payload without sub
        mock_jwt_decode.return_value = {"exp": 123456789}
        
        # Call the function and check it raises
        with pytest.raises(AuthenticationError) as excinfo:
            await get_current_user("invalid_token")
        
        assert "Could not validate credentials" in str(excinfo.value)
    
    @pytest.mark.asyncio
    @patch('camera_collector.core.security.jwt.decode')
    async def test_get_current_user_jwt_error(self, mock_jwt_decode):
        """Test get_current_user with JWT error."""
        # Mock JWT decode to raise an error
        mock_jwt_decode.side_effect = JWTError("Invalid token")
        
        # Call the function and check it raises
        with pytest.raises(AuthenticationError) as excinfo:
            await get_current_user("invalid_token")
        
        assert "Could not validate credentials" in str(excinfo.value)