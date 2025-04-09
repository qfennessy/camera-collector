import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import pytest_asyncio

from camera_collector.services.camera_service import CameraService
from camera_collector.schemas.camera import CameraCreate, CameraUpdate
from camera_collector.models.camera import Camera
from camera_collector.core.exceptions import NotFoundError


@pytest.mark.asyncio
class TestCameraService:
    """Test camera service."""
    
    @pytest_asyncio.fixture
    async def mock_repo(self):
        """Mock camera repository fixture."""
        repository = AsyncMock()
        return repository
    
    @pytest_asyncio.fixture
    async def camera_service(self, mock_repo):
        """Camera service fixture."""
        return CameraService(mock_repo)
    
    @pytest_asyncio.fixture
    async def sample_camera_data(self):
        """Sample camera data fixture."""
        return CameraCreate(
            brand="Nikon",
            model="F3",
            year_manufactured=1980,
            type="SLR",
            film_format="35mm",
            condition="excellent"
        )
    
    async def test_create_camera(self, camera_service, mock_repo, sample_camera_data):
        """Test creating a camera."""
        # Setup mock
        mock_camera = Camera(
            id="123",
            brand=sample_camera_data.brand,
            model=sample_camera_data.model,
            year_manufactured=sample_camera_data.year_manufactured,
            type=sample_camera_data.type,
            film_format=sample_camera_data.film_format,
            condition=sample_camera_data.condition
        )
        mock_repo.create.return_value = mock_camera
        
        # Call service
        result = await camera_service.create_camera(sample_camera_data)
        
        # Assert
        mock_repo.create.assert_called_once()
        assert result.brand == sample_camera_data.brand
        assert result.model == sample_camera_data.model
    
    async def test_get_camera(self, camera_service, mock_repo):
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
        mock_repo.get_by_id.return_value = mock_camera
        
        # Call service
        result = await camera_service.get_camera(camera_id)
        
        # Assert
        mock_repo.get_by_id.assert_called_once_with(camera_id)
        assert result.id == camera_id
        assert result.brand == mock_camera.brand
    
    async def test_get_camera_not_found(self, camera_service, mock_repo):
        """Test getting a non-existent camera."""
        # Setup mock
        camera_id = "123"
        mock_repo.get_by_id.side_effect = NotFoundError(f"Camera with ID {camera_id} not found")
        
        # Assert
        with pytest.raises(NotFoundError):
            await camera_service.get_camera(camera_id)
    
    async def test_get_cameras(self, camera_service, mock_repo):
        """Test getting all cameras."""
        # Setup mock
        mock_cameras = [
            Camera(
                id="123",
                brand="Nikon",
                model="F3",
                year_manufactured=1980,
                type="SLR",
                film_format="35mm",
                condition="excellent"
            ),
            Camera(
                id="456",
                brand="Leica",
                model="M3",
                year_manufactured=1954,
                type="rangefinder",
                film_format="35mm",
                condition="good"
            )
        ]
        mock_repo.get_all.return_value = mock_cameras
        mock_repo.count.return_value = len(mock_cameras)
        
        # Call service
        result = await camera_service.get_cameras()
        
        # Assert
        mock_repo.get_all.assert_called_once()
        mock_repo.count.assert_called_once()
        assert result.total == 2
        assert len(result.items) == 2
    
    async def test_update_camera(self, camera_service, mock_repo):
        """Test updating a camera."""
        # Setup mocks
        camera_id = "123"
        existing_camera = Camera(
            id=camera_id,
            brand="Nikon",
            model="F3",
            year_manufactured=1980,
            type="SLR",
            film_format="35mm",
            condition="excellent"
        )
        
        update_data = CameraUpdate(notes="Test notes")
        
        # Mocks
        mock_repo.get_by_id.return_value = existing_camera
        
        updated_camera = Camera(
            id=camera_id,
            brand=existing_camera.brand,
            model=existing_camera.model,
            year_manufactured=existing_camera.year_manufactured,
            type=existing_camera.type,
            film_format=existing_camera.film_format,
            condition=existing_camera.condition,
            notes="Test notes"
        )
        mock_repo.update.return_value = updated_camera
        
        # Call service
        result = await camera_service.update_camera(camera_id, update_data)
        
        # Assert
        mock_repo.get_by_id.assert_called_once_with(camera_id)
        mock_repo.update.assert_called_once()
        assert result.notes == "Test notes"
    
    async def test_delete_camera(self, camera_service, mock_repo):
        """Test deleting a camera."""
        # Setup mock
        camera_id = "123"
        mock_repo.delete.return_value = True
        
        # Call service
        result = await camera_service.delete_camera(camera_id)
        
        # Assert
        mock_repo.delete.assert_called_once_with(camera_id)
        assert result is True