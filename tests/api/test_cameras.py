import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from camera_collector.main import app
from camera_collector.services.camera_service import CameraService
from camera_collector.models.camera import Camera
from camera_collector.schemas.camera import CameraListResponse
from camera_collector.core.exceptions import NotFoundError


# Patch dependencies to use mocked services
@pytest.fixture
def mock_camera_service():
    """Mock camera service."""
    return AsyncMock(spec=CameraService)


@pytest.fixture
def client(mock_camera_service):
    """Test client with mocked dependencies."""
    
    app.dependency_overrides = {}
    
    # Mock camera service
    async def override_get_camera_service():
        return mock_camera_service
    
    # Mock get_current_user_id
    async def override_get_current_user_id():
        return "test_user_id"
    
    from camera_collector.api.dependencies import get_camera_service, get_current_user_id
    app.dependency_overrides[get_camera_service] = override_get_camera_service
    app.dependency_overrides[get_current_user_id] = override_get_current_user_id
    
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.asyncio
class TestCamerasRouter:
    """Test cameras router."""
    
    async def test_get_cameras(self, client, mock_camera_service):
        """Test getting all cameras."""
        # Setup mock
        mock_camera1 = Camera(
            id="123",
            brand="Nikon",
            model="F3",
            year_manufactured=1980,
            type="SLR",
            film_format="35mm",
            condition="excellent"
        )
        mock_camera2 = Camera(
            id="456",
            brand="Leica",
            model="M3",
            year_manufactured=1954,
            type="rangefinder",
            film_format="35mm",
            condition="good"
        )
        
        # Mock the CameraListResponse
        mock_response = CameraListResponse(
            items=[mock_camera1, mock_camera2],
            total=2,
            page=1,
            size=10,
            pages=1
        )
        mock_camera_service.get_cameras.return_value = mock_response
        
        # Call endpoint
        response = client.get("/api/cameras")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2
        assert data["items"][0]["brand"] == "Nikon"
        assert data["items"][1]["brand"] == "Leica"
        
        # Verify service call
        mock_camera_service.get_cameras.assert_awaited_once()
    
    async def test_create_camera(self, client, mock_camera_service):
        """Test creating a camera."""
        # Setup mock
        camera_data = {
            "brand": "Nikon",
            "model": "F3",
            "year_manufactured": 1980,
            "type": "SLR",
            "film_format": "35mm",
            "condition": "excellent"
        }
        
        mock_camera = Camera(
            id="123",
            **camera_data
        )
        mock_camera_service.create_camera.return_value = mock_camera
        
        # Call endpoint
        response = client.post(
            "/api/cameras",
            json=camera_data
        )
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["brand"] == camera_data["brand"]
        assert data["model"] == camera_data["model"]
        assert "id" in data
        
        # Verify service call
        mock_camera_service.create_camera.assert_awaited_once()
    
    async def test_get_camera(self, client, mock_camera_service):
        """Test getting a camera by ID."""
        # Setup mock
        camera_id = "123"
        mock_camera = Camera(
            id=camera_id,
            brand="Nikon",
            model="F3",
            year_manufactured=1980,
            type="SLR",
            film_format="35mm",
            condition="excellent"
        )
        mock_camera_service.get_camera.return_value = mock_camera
        
        # Call endpoint
        response = client.get(f"/api/cameras/{camera_id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == camera_id
        assert data["brand"] == "Nikon"
        assert data["model"] == "F3"
        
        # Verify service call
        mock_camera_service.get_camera.assert_awaited_once_with(camera_id)
    
    async def test_get_camera_not_found(self, client, mock_camera_service):
        """Test getting a non-existent camera."""
        # Setup mock
        camera_id = "123"
        mock_camera_service.get_camera.side_effect = NotFoundError(f"Camera with ID {camera_id} not found")
        
        # Call endpoint
        response = client.get(f"/api/cameras/{camera_id}")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert f"Camera with ID {camera_id} not found" in data["detail"]
    
    async def test_update_camera(self, client, mock_camera_service):
        """Test updating a camera."""
        # Setup mock
        camera_id = "123"
        update_data = {
            "notes": "Test notes"
        }
        
        mock_camera = Camera(
            id=camera_id,
            brand="Nikon",
            model="F3",
            year_manufactured=1980,
            type="SLR",
            film_format="35mm",
            condition="excellent",
            notes="Test notes"
        )
        mock_camera_service.update_camera.return_value = mock_camera
        
        # Call endpoint
        response = client.put(
            f"/api/cameras/{camera_id}",
            json=update_data
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == camera_id
        assert data["notes"] == "Test notes"
        
        # Verify service call
        mock_camera_service.update_camera.assert_awaited_once()
    
    async def test_update_camera_not_found(self, client, mock_camera_service):
        """Test updating a non-existent camera."""
        # Setup mock
        camera_id = "123"
        update_data = {
            "notes": "Test notes"
        }
        
        mock_camera_service.update_camera.side_effect = NotFoundError(f"Camera with ID {camera_id} not found")
        
        # Call endpoint
        response = client.put(
            f"/api/cameras/{camera_id}",
            json=update_data
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert f"Camera with ID {camera_id} not found" in data["detail"]
    
    async def test_delete_camera(self, client, mock_camera_service):
        """Test deleting a camera."""
        # Setup mock
        camera_id = "123"
        mock_camera_service.delete_camera.return_value = True
        
        # Call endpoint
        response = client.delete(f"/api/cameras/{camera_id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verify service call
        mock_camera_service.delete_camera.assert_awaited_once_with(camera_id)
    
    async def test_delete_camera_not_found(self, client, mock_camera_service):
        """Test deleting a non-existent camera."""
        # Setup mock
        camera_id = "123"
        mock_camera_service.delete_camera.side_effect = NotFoundError(f"Camera with ID {camera_id} not found")
        
        # Call endpoint
        response = client.delete(f"/api/cameras/{camera_id}")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert f"Camera with ID {camera_id} not found" in data["detail"]