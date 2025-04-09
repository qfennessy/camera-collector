import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from camera_collector.main import app
from camera_collector.services.auth_service import AuthService
from camera_collector.models.user import User
from camera_collector.schemas.auth import TokenResponse
from camera_collector.core.exceptions import ValidationError, AuthenticationError


# Patch dependencies to use mocked services
@pytest.fixture
def mock_auth_service():
    """Mock auth service."""
    return AsyncMock(spec=AuthService)


@pytest.fixture
def client(mock_auth_service):
    """Test client with mocked dependencies."""
    
    app.dependency_overrides = {}
    
    # Mock auth service
    async def override_get_auth_service():
        return mock_auth_service
    
    # Mock get_current_user_id
    async def override_get_current_user_id():
        return "test_user_id"
    
    from camera_collector.api.dependencies import get_auth_service, get_current_user_id
    app.dependency_overrides[get_auth_service] = override_get_auth_service
    app.dependency_overrides[get_current_user_id] = override_get_current_user_id
    
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.asyncio
class TestAuthRouter:
    """Test auth router."""
    
    async def test_register_user(self, client, mock_auth_service):
        """Test registering a new user."""
        # Setup mock
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        
        mock_user = User(
            id="123",
            username=user_data["username"],
            email=user_data["email"],
            hashed_password="hashed_password"
        )
        mock_auth_service.register_user.return_value = mock_user
        
        # Call endpoint
        response = client.post(
            "/api/auth/register",
            json=user_data
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert "id" in data
        assert "hashed_password" not in data
        
        # Verify service call
        mock_auth_service.register_user.assert_awaited_once()
    
    async def test_register_user_validation_error(self, client, mock_auth_service):
        """Test registering a user with validation error."""
        # Setup mock
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        
        mock_auth_service.register_user.side_effect = ValidationError("Username already exists")
        
        # Call endpoint
        response = client.post(
            "/api/auth/register",
            json=user_data
        )
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert "Username already exists" in data["detail"]
    
    async def test_login(self, client, mock_auth_service):
        """Test login."""
        # Setup mock
        mock_token = TokenResponse(
            access_token="access_token",
            refresh_token="refresh_token"
        )
        mock_auth_service.login.return_value = mock_token
        
        # Call endpoint
        response = client.post(
            "/api/auth/login",
            data={
                "username": "testuser",
                "password": "password123"
            }
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] == "access_token"
        assert data["refresh_token"] == "refresh_token"
        assert data["token_type"] == "bearer"
        
        # Verify service call
        mock_auth_service.login.assert_awaited_once_with("testuser", "password123")
    
    async def test_login_authentication_error(self, client, mock_auth_service):
        """Test login with authentication error."""
        # Setup mock
        mock_auth_service.login.side_effect = AuthenticationError("Invalid credentials")
        
        # Call endpoint
        response = client.post(
            "/api/auth/login",
            data={
                "username": "testuser",
                "password": "password123"
            }
        )
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "Invalid credentials" in data["detail"]
    
    async def test_refresh_token(self, client, mock_auth_service):
        """Test refresh token."""
        # Setup mock
        mock_token = TokenResponse(
            access_token="new_access_token",
            refresh_token="new_refresh_token"
        )
        mock_auth_service.refresh_token.return_value = mock_token
        
        # Call endpoint
        response = client.post(
            "/api/auth/refresh",
            json={
                "refresh_token": "refresh_token"
            }
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] == "new_access_token"
        assert data["refresh_token"] == "new_refresh_token"
        assert data["token_type"] == "bearer"
        
        # Verify service call
        mock_auth_service.refresh_token.assert_awaited_once_with("refresh_token")
    
    async def test_refresh_token_authentication_error(self, client, mock_auth_service):
        """Test refresh token with authentication error."""
        # Setup mock
        mock_auth_service.refresh_token.side_effect = AuthenticationError("Invalid token")
        
        # Call endpoint
        response = client.post(
            "/api/auth/refresh",
            json={
                "refresh_token": "refresh_token"
            }
        )
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert "Invalid token" in data["detail"]