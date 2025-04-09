import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
import os
from typing import Dict, Any
import uuid

from camera_collector.main import app
from camera_collector.db.database import connect_to_mongodb, close_mongodb_connection
from camera_collector.schemas.user import UserCreate
from camera_collector.services.auth_service import AuthService
from camera_collector.api.dependencies import get_auth_service
from camera_collector.db.repositories.user_repository import UserRepository
from camera_collector.db.database import db


# Skip this integration test if MongoDB is not available
pytestmark = pytest.mark.skip("Integration tests require MongoDB setup")


@pytest.fixture(scope="module")
async def setup_db():
    """Set up the database connection for testing."""
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


@pytest.fixture
def test_client(setup_db):
    """Test client with real database."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
async def auth_service():
    """Create a real auth service for testing."""
    user_repo = UserRepository(db.db)
    return AuthService(user_repo)


@pytest.fixture
async def test_user(auth_service) -> Dict[str, Any]:
    """Create a test user and return user data."""
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    
    # Try to create user if it doesn't exist
    try:
        user = await auth_service.register_user(user_data)
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    except Exception:
        # User might already exist, try to authenticate instead
        tokens = await auth_service.login(user_data.username, user_data.password)
        return {
            "username": user_data.username,
            "email": user_data.email,
            "access_token": tokens.access_token
        }


@pytest_asyncio.fixture
async def auth_header(test_client, test_user):
    """Get authentication header with valid token."""
    login_response = test_client.post(
        "/api/auth/login",
        data={
            "username": test_user["username"],
            "password": "password123"
        }
    )
    access_token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest_asyncio.fixture
async def test_camera(test_client, auth_header):
    """Create a test camera and return its data."""
    camera_data = {
        "brand": "Test Brand",
        "model": "Test Model",
        "year_manufactured": 2000,
        "type": "Test Type",
        "film_format": "35mm",
        "condition": "excellent"
    }
    
    create_response = test_client.post(
        "/api/cameras",
        json=camera_data,
        headers=auth_header
    )
    
    camera = create_response.json()
    yield camera
    
    # Clean up - delete the camera
    test_client.delete(
        f"/api/cameras/{camera['id']}",
        headers=auth_header
    )


@pytest.mark.asyncio
@pytest.mark.integration
class TestAPIIntegration:
    """Integration tests for the API."""
    
    async def test_register_and_login(self, test_client):
        """Test registering a new user and logging in."""
        # Generate a unique username and email
        unique_id = str(uuid.uuid4())[:8]
        username = f"testuser_{unique_id}"
        email = f"test_{unique_id}@example.com"
        
        # Register a new user
        register_response = test_client.post(
            "/api/auth/register",
            json={
                "username": username,
                "email": email,
                "password": "password123"
            }
        )
        
        # Check registration
        assert register_response.status_code == 201
        user_data = register_response.json()
        assert user_data["username"] == username
        assert user_data["email"] == email
        
        # Login with the created user
        login_response = test_client.post(
            "/api/auth/login",
            data={
                "username": username,
                "password": "password123"
            }
        )
        
        # Check login
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert "refresh_token" in token_data
    
    async def test_create_and_get_camera(self, test_client, auth_header):
        """Test creating and retrieving a camera."""
        # Create a camera
        camera_data = {
            "brand": "Test Brand",
            "model": "Test Model",
            "year_manufactured": 2000,
            "type": "Test Type",
            "film_format": "35mm",
            "condition": "excellent"
        }
        
        create_response = test_client.post(
            "/api/cameras",
            json=camera_data,
            headers=auth_header
        )
        
        # Check camera creation
        assert create_response.status_code == 201
        created_camera = create_response.json()
        assert created_camera["brand"] == camera_data["brand"]
        assert created_camera["model"] == camera_data["model"]
        
        # Get the created camera
        camera_id = created_camera["id"]
        get_response = test_client.get(
            f"/api/cameras/{camera_id}",
            headers=auth_header
        )
        
        # Check camera retrieval
        assert get_response.status_code == 200
        retrieved_camera = get_response.json()
        assert retrieved_camera["id"] == camera_id
        assert retrieved_camera["brand"] == camera_data["brand"]
        
        # Clean up - delete the camera
        delete_response = test_client.delete(
            f"/api/cameras/{camera_id}",
            headers=auth_header
        )
        assert delete_response.status_code == 204
    
    async def test_update_camera(self, test_client, auth_header, test_camera):
        """Test updating a camera."""
        # Update camera data
        update_data = {
            "condition": "good",
            "notes": "Test notes for update"
        }
        
        update_response = test_client.patch(
            f"/api/cameras/{test_camera['id']}",
            json=update_data,
            headers=auth_header
        )
        
        # Check update response
        assert update_response.status_code == 200
        updated_camera = update_response.json()
        assert updated_camera["id"] == test_camera["id"]
        assert updated_camera["condition"] == "good"
        assert updated_camera["notes"] == "Test notes for update"
        # Original data should remain unchanged
        assert updated_camera["brand"] == test_camera["brand"]
        assert updated_camera["model"] == test_camera["model"]
    
    async def test_list_cameras(self, test_client, auth_header, test_camera):
        """Test listing cameras with pagination."""
        # Get cameras with default pagination
        list_response = test_client.get(
            "/api/cameras",
            headers=auth_header
        )
        
        # Check list response
        assert list_response.status_code == 200
        result = list_response.json()
        assert "items" in result
        assert "total" in result
        assert "page" in result
        assert "size" in result
        assert result["page"] == 1
        assert result["size"] == 10
        assert result["total"] >= 1
        
        # Check if our test camera is in the list
        camera_ids = [cam["id"] for cam in result["items"]]
        assert test_camera["id"] in camera_ids
        
        # Test pagination
        pagination_response = test_client.get(
            "/api/cameras?page=1&size=5",
            headers=auth_header
        )
        
        # Check pagination response
        assert pagination_response.status_code == 200
        pagination_result = pagination_response.json()
        assert pagination_result["size"] == 5
    
    async def test_camera_statistics(self, test_client, auth_header, test_camera):
        """Test camera statistics endpoints."""
        # Test brand statistics
        brand_stats_response = test_client.get(
            "/api/stats/brands",
            headers=auth_header
        )
        assert brand_stats_response.status_code == 200
        brand_stats = brand_stats_response.json()
        assert len(brand_stats) >= 1
        
        # Test type statistics
        type_stats_response = test_client.get(
            "/api/stats/types",
            headers=auth_header
        )
        assert type_stats_response.status_code == 200
        type_stats = type_stats_response.json()
        assert len(type_stats) >= 1
        
        # Test decade statistics
        decade_stats_response = test_client.get(
            "/api/stats/decades",
            headers=auth_header
        )
        assert decade_stats_response.status_code == 200
        decade_stats = decade_stats_response.json()
        assert len(decade_stats) >= 1
        
        # Test total value
        value_response = test_client.get(
            "/api/stats/value",
            headers=auth_header
        )
        assert value_response.status_code == 200
        value_data = value_response.json()
        assert "total_value" in value_data
    
    async def test_token_refresh(self, test_client, auth_header):
        """Test token refresh functionality."""
        # Login to get refresh token
        login_response = test_client.post(
            "/api/auth/login",
            data={
                "username": "testuser",
                "password": "password123"
            }
        )
        
        refresh_token = login_response.json()["refresh_token"]
        
        # Use refresh token to get new access token
        refresh_response = test_client.post(
            "/api/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        # Check refresh response
        assert refresh_response.status_code == 200
        token_data = refresh_response.json()
        assert "access_token" in token_data
        assert "refresh_token" in token_data
    
    async def test_invalid_auth(self, test_client):
        """Test invalid authentication."""
        # Try to access protected endpoint without token
        no_token_response = test_client.get("/api/cameras")
        assert no_token_response.status_code == 401
        
        # Try to access protected endpoint with invalid token
        invalid_token_response = test_client.get(
            "/api/cameras",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert invalid_token_response.status_code == 401