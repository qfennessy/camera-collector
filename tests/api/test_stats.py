import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from camera_collector.main import app
from camera_collector.services.camera_service import CameraService
from camera_collector.schemas.camera import BrandStats, TypeStats, DecadeStats, ValueStats
from camera_collector.core.exceptions import DatabaseError


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
class TestStatsRouter:
    """Test statistics router."""
    
    async def test_get_stats_by_brand(self, client, mock_camera_service):
        """Test getting camera statistics by brand."""
        # Setup mock
        mock_stats = [
            BrandStats(brand="Nikon", count=5),
            BrandStats(brand="Leica", count=3),
            BrandStats(brand="Canon", count=2)
        ]
        mock_camera_service.get_stats_by_brand.return_value = mock_stats
        
        # Call endpoint
        response = client.get("/api/stats/brands")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["brand"] == "Nikon"
        assert data[0]["count"] == 5
        assert data[1]["brand"] == "Leica"
        assert data[1]["count"] == 3
        
        # Verify service call
        mock_camera_service.get_stats_by_brand.assert_awaited_once()
    
    async def test_get_stats_by_brand_error(self, client, mock_camera_service):
        """Test getting camera statistics by brand with error."""
        # Setup mock
        mock_camera_service.get_stats_by_brand.side_effect = DatabaseError("Database error")
        
        # Call endpoint
        response = client.get("/api/stats/brands")
        
        # Assert
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "Database error" in data["detail"]
    
    async def test_get_stats_by_type(self, client, mock_camera_service):
        """Test getting camera statistics by type."""
        # Setup mock
        mock_stats = [
            TypeStats(type="SLR", count=4),
            TypeStats(type="rangefinder", count=3),
            TypeStats(type="medium format", count=2)
        ]
        mock_camera_service.get_stats_by_type.return_value = mock_stats
        
        # Call endpoint
        response = client.get("/api/stats/types")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["type"] == "SLR"
        assert data[0]["count"] == 4
        assert data[1]["type"] == "rangefinder"
        assert data[1]["count"] == 3
        
        # Verify service call
        mock_camera_service.get_stats_by_type.assert_awaited_once()
    
    async def test_get_stats_by_decade(self, client, mock_camera_service):
        """Test getting camera statistics by decade."""
        # Setup mock
        mock_stats = [
            DecadeStats(decade="1950s", count=2),
            DecadeStats(decade="1960s", count=1),
            DecadeStats(decade="1970s", count=3),
            DecadeStats(decade="1980s", count=4)
        ]
        mock_camera_service.get_stats_by_decade.return_value = mock_stats
        
        # Call endpoint
        response = client.get("/api/stats/decades")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4
        assert data[0]["decade"] == "1950s"
        assert data[0]["count"] == 2
        assert data[3]["decade"] == "1980s"
        assert data[3]["count"] == 4
        
        # Verify service call
        mock_camera_service.get_stats_by_decade.assert_awaited_once()
    
    async def test_get_total_value(self, client, mock_camera_service):
        """Test getting total value of all cameras."""
        # Setup mock
        mock_value = ValueStats(total_value=5000.0)
        mock_camera_service.get_total_value.return_value = mock_value
        
        # Call endpoint
        response = client.get("/api/stats/value")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["total_value"] == 5000.0
        
        # Verify service call
        mock_camera_service.get_total_value.assert_awaited_once()