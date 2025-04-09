import pytest
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from camera_collector.core.exceptions import (
    NotFoundError,
    DatabaseError,
    AuthenticationError,
    AuthorizationError,
    ValidationError
)


class TestExceptions:
    """Test exception handling."""
    
    def test_not_found_error(self):
        """Test NotFoundError exception."""
        message = "Camera not found"
        error = NotFoundError(message)
        
        assert error.status_code == status.HTTP_404_NOT_FOUND
        assert error.detail == message
        assert isinstance(error, HTTPException)
    
    def test_database_error(self):
        """Test DatabaseError exception."""
        message = "Database connection failed"
        error = DatabaseError(message)
        
        assert error.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert error.detail == message
        assert isinstance(error, HTTPException)
    
    def test_authentication_error(self):
        """Test AuthenticationError exception."""
        message = "Invalid credentials"
        error = AuthenticationError(message)
        
        assert error.status_code == status.HTTP_401_UNAUTHORIZED
        assert error.detail == message
        assert isinstance(error, HTTPException)
        assert error.headers == {"WWW-Authenticate": "Bearer"}
    
    def test_authorization_error(self):
        """Test AuthorizationError exception."""
        message = "Not authorized to access this resource"
        error = AuthorizationError(message)
        
        assert error.status_code == status.HTTP_403_FORBIDDEN
        assert error.detail == message
        assert isinstance(error, HTTPException)
    
    def test_validation_error(self):
        """Test ValidationError exception."""
        message = "Invalid camera data"
        error = ValidationError(message)
        
        assert error.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert error.detail == message
        assert isinstance(error, HTTPException)