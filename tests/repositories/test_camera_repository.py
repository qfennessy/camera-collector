import pytest
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
import pytest_asyncio

from camera_collector.db.repositories.camera_repository import CameraRepository
from camera_collector.models.camera import Camera
from camera_collector.core.exceptions import NotFoundError


@pytest.mark.asyncio
class TestCameraRepository:
    """Test camera repository."""
    
    @pytest_asyncio.fixture
    async def camera_repo(self, mongodb):
        """Camera repository fixture."""
        return CameraRepository(mongodb)
    
    @pytest_asyncio.fixture
    async def sample_camera(self):
        """Sample camera data fixture."""
        return Camera(
            brand="Nikon",
            model="F3",
            year_manufactured=1980,
            type="SLR",
            film_format="35mm",
            condition="excellent"
        )
    
    @pytest_asyncio.fixture
    async def created_camera(self, camera_repo, sample_camera):
        """Fixture to create a camera and clean up after test."""
        camera = await camera_repo.create(sample_camera)
        yield camera
        try:
            await camera_repo.delete(camera.id)
        except:
            pass
    
    async def test_create_camera(self, camera_repo, sample_camera):
        """Test creating a camera."""
        camera = await camera_repo.create(sample_camera)
        
        assert camera.id is not None
        assert camera.brand == sample_camera.brand
        assert camera.model == sample_camera.model
        
        # Clean up
        await camera_repo.delete(camera.id)
    
    async def test_get_camera_by_id(self, camera_repo, created_camera):
        """Test getting a camera by ID."""
        camera = await camera_repo.get_by_id(created_camera.id)
        
        assert camera is not None
        assert camera.id == created_camera.id
        assert camera.brand == created_camera.brand
        assert camera.model == created_camera.model
    
    async def test_get_camera_by_id_not_found(self, camera_repo):
        """Test getting a non-existent camera."""
        with pytest.raises(NotFoundError):
            await camera_repo.get_by_id(str(ObjectId()))
    
    async def test_get_all_cameras(self, camera_repo, created_camera):
        """Test getting all cameras."""
        cameras = await camera_repo.get_all()
        
        assert len(cameras) >= 1
        assert any(c.id == created_camera.id for c in cameras)
    
    async def test_update_camera(self, camera_repo, created_camera):
        """Test updating a camera."""
        # Update the camera
        created_camera.notes = "Test notes"
        updated_camera = await camera_repo.update(created_camera.id, created_camera)
        
        assert updated_camera.notes == "Test notes"
        
        # Verify update in database
        camera = await camera_repo.get_by_id(created_camera.id)
        assert camera.notes == "Test notes"
    
    async def test_update_camera_not_found(self, camera_repo, sample_camera):
        """Test updating a non-existent camera."""
        with pytest.raises(NotFoundError):
            await camera_repo.update(str(ObjectId()), sample_camera)
    
    async def test_delete_camera(self, camera_repo, created_camera):
        """Test deleting a camera."""
        result = await camera_repo.delete(created_camera.id)
        
        assert result is True
        
        # Verify camera is deleted
        with pytest.raises(NotFoundError):
            await camera_repo.get_by_id(created_camera.id)
    
    async def test_delete_camera_not_found(self, camera_repo):
        """Test deleting a non-existent camera."""
        with pytest.raises(NotFoundError):
            await camera_repo.delete(str(ObjectId()))