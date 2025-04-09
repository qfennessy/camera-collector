import pytest
from unittest.mock import AsyncMock, patch
import pytest_asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

from camera_collector.db.repositories.camera_repository import CameraRepository
from camera_collector.models.camera import Camera, CameraCreate, CameraUpdate
from camera_collector.core.exceptions import NotFoundError
from camera_collector.core.config import settings


@pytest.mark.integration
@pytest.mark.asyncio
class TestCameraRepository:
    """Test the camera repository with MongoDB."""
    
    # Create a direct fixture for repository that doesn't use mongodb fixture
    @pytest_asyncio.fixture
    async def camera_repo(self, mongodb_available):
        """Create a CameraRepository instance."""
        if not mongodb_available:
            pytest.skip("MongoDB is not available")
            
        # Create a direct connection to MongoDB
        mongo_url = os.environ.get("MONGODB_TEST_URL", settings.MONGODB_TEST_URL)
        mongo_db = os.environ.get("MONGODB_TEST_DB", settings.MONGODB_TEST_DB)
        
        # Create a real client
        client = AsyncIOMotorClient(mongo_url)
        db = client[mongo_db]
        
        # Clean up before test
        await db.cameras.delete_many({})
        
        # Create and return the repository
        repo = CameraRepository(db)
        
        yield repo
        
        # Clean up after test
        await db.cameras.delete_many({})
        client.close()
    
    async def test_create_camera(self, camera_repo, mongodb_available):
        """Test creating a new camera."""
        if not mongodb_available:
            pytest.skip("MongoDB is not available")
        
        # Create a test camera (using Camera directly instead of CameraCreate)
        camera_data = Camera(
            # Don't set ID, let MongoDB generate it
            brand="Test Brand",
            model="Test Model",
            year_manufactured=2020,
            type="SLR",
            film_format="35mm",
            condition="excellent"
        )
        
        # Create the camera
        camera = await camera_repo.create(camera_data)
        
        # Check that it was created
        assert camera.id is not None
        assert camera.brand == "Test Brand"
        assert camera.model == "Test Model"
        
        # No need to clean up here as the fixture will clean up
    
    async def test_get_camera(self, camera_repo, mongodb_available):
        """Test getting a camera by ID."""
        if not mongodb_available:
            pytest.skip("MongoDB is not available")
        
        # Create a test camera
        camera_data = Camera(
            # Don't set ID, let MongoDB generate it
            brand="Test Brand",
            model="Test Model",
            year_manufactured=2020,
            type="SLR",
            film_format="35mm",
            condition="excellent"
        )
        camera = await camera_repo.create(camera_data)
        
        # Get the camera by ID
        retrieved_camera = await camera_repo.get_by_id(camera.id)
        
        # Check that it matches
        assert retrieved_camera.id == camera.id
        assert retrieved_camera.brand == camera.brand
        assert retrieved_camera.model == camera.model
        
        # No need to clean up here as the fixture will clean up
    
    async def test_update_camera(self, camera_repo, mongodb_available):
        """Test updating a camera."""
        if not mongodb_available:
            pytest.skip("MongoDB is not available")
        
        # Create a test camera
        camera_data = Camera(
            # Don't set ID, let MongoDB generate it
            brand="Test Brand",
            model="Test Model",
            year_manufactured=2020,
            type="SLR",
            film_format="35mm",
            condition="excellent"
        )
        camera = await camera_repo.create(camera_data)
        
        # Convert CameraUpdate to a dict
        update_data = {"condition": "mint"}
        updated_camera = await camera_repo.update_by_id(camera.id, update_data)
        
        # Check that it was updated
        assert updated_camera.id == camera.id
        assert updated_camera.condition == "mint"
        
        # No need to clean up here as the fixture will clean up
    
    async def test_delete_camera(self, camera_repo, mongodb_available):
        """Test deleting a camera."""
        if not mongodb_available:
            pytest.skip("MongoDB is not available")
        
        # Create a test camera
        camera_data = Camera(
            # Don't set ID, let MongoDB generate it
            brand="Test Brand",
            model="Test Model",
            year_manufactured=2020,
            type="SLR",
            film_format="35mm",
            condition="excellent"
        )
        camera = await camera_repo.create(camera_data)
        
        # Delete the camera
        await camera_repo.delete_by_id(camera.id)
        
        # Try to get the camera (should raise NotFoundError)
        with pytest.raises(NotFoundError):
            await camera_repo.get_by_id(camera.id)