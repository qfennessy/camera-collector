import pytest
from unittest.mock import AsyncMock, MagicMock, patch, Mock
import pytest_asyncio
from bson import ObjectId

from camera_collector.db.repositories.camera_repository import CameraRepository
from camera_collector.models.camera import Camera
from camera_collector.core.exceptions import NotFoundError


# We'll skip the real database tests since they require an actual MongoDB instance
# This demonstrates how we would set up mock-based tests for the repository
@pytest.mark.asyncio
class TestCameraRepositoryMock:
    """Test camera repository with mocked MongoDB."""
    
    @pytest_asyncio.fixture
    async def mock_db(self):
        """Mock MongoDB database."""
        db = AsyncMock()
        db.cameras = AsyncMock()
        return db
    
    @pytest_asyncio.fixture
    async def camera_repo(self, mock_db):
        """Camera repository fixture with mocked database."""
        repo = CameraRepository(mock_db)
        return repo
    
    @pytest_asyncio.fixture
    async def sample_camera(self):
        """Sample camera data fixture."""
        # Use None for ID to avoid ObjectId validation issues
        camera = Camera(
            brand="Nikon",
            model="F3",
            year_manufactured=1980,
            type="SLR",
            film_format="35mm",
            condition="excellent"
        )
        camera.id = None  # Make sure ID is None for testing
        return camera
    
    async def test_create_camera(self, camera_repo, mock_db, sample_camera):
        """Test creating a camera."""
        # Setup mock
        object_id = ObjectId()
        mock_result = AsyncMock()
        mock_result.inserted_id = object_id
        mock_db.cameras.insert_one.return_value = mock_result
        
        # Call repository
        camera = await camera_repo.create(sample_camera)
        
        # Assert
        mock_db.cameras.insert_one.assert_called_once()
        assert camera.id == str(object_id)
        assert camera.brand == sample_camera.brand
        assert camera.model == sample_camera.model
    
    async def test_get_camera_by_id(self, camera_repo, mock_db):
        """Test getting a camera by ID."""
        # Setup mock
        object_id = ObjectId()
        camera_id = str(object_id)
        
        with patch('bson.objectid.ObjectId', return_value=object_id):
            mock_db.cameras.find_one.return_value = {
                "_id": object_id,
                "brand": "Nikon",
                "model": "F3",
                "year_manufactured": 1980,
                "type": "SLR",
                "film_format": "35mm",
                "condition": "excellent"
            }
            
            # Call repository
            camera = await camera_repo.get_by_id(camera_id)
            
            # Assert
            mock_db.cameras.find_one.assert_called_once()
            assert camera.id == camera_id
            assert camera.brand == "Nikon"
            assert camera.model == "F3"
    
    async def test_get_camera_by_id_not_found(self, camera_repo, mock_db):
        """Test getting a non-existent camera."""
        # Setup mock
        object_id = ObjectId()
        camera_id = str(object_id)
        
        with patch('bson.objectid.ObjectId', return_value=object_id):
            mock_db.cameras.find_one.return_value = None
            
            # Assert
            with pytest.raises(NotFoundError):
                await camera_repo.get_by_id(camera_id)
    
    async def test_get_all_cameras(self, camera_repo, mock_db):
        """Test getting all cameras."""
        # Create proper mock for cursor with skip/limit methods
        mock_cursor = AsyncMock()
        mock_db.cameras.find.return_value = mock_cursor
        
        skip_mock = AsyncMock()
        mock_cursor.skip.return_value = skip_mock
        
        limit_mock = AsyncMock()
        skip_mock.limit.return_value = limit_mock
        
        # Setup async iterator for cursor
        object_id1 = ObjectId()
        object_id2 = ObjectId()
        limit_mock.__aiter__.return_value = [
            {"_id": object_id1, "brand": "Nikon", "model": "F3", 
             "year_manufactured": 1980, "type": "SLR", 
             "film_format": "35mm", "condition": "excellent"},
            {"_id": object_id2, "brand": "Leica", "model": "M3", 
             "year_manufactured": 1954, "type": "rangefinder", 
             "film_format": "35mm", "condition": "good"}
        ]
        
        # Call repository
        cameras = await camera_repo.get_all()
        
        # Assert
        mock_db.cameras.find.assert_called_once()
        assert len(cameras) == 2
        assert cameras[0].id == str(object_id1)
        assert cameras[0].brand == "Nikon"
        assert cameras[1].id == str(object_id2)
        assert cameras[1].brand == "Leica"
    
    async def test_count_cameras(self, camera_repo, mock_db):
        """Test counting cameras."""
        # Setup mock
        mock_db.cameras.count_documents.return_value = 5
        
        # Call repository
        count = await camera_repo.count()
        
        # Assert
        mock_db.cameras.count_documents.assert_called_once_with({})
        assert count == 5
    
    async def test_update_camera(self, camera_repo, mock_db, sample_camera):
        """Test updating a camera."""
        # Setup mock
        object_id = ObjectId()
        camera_id = str(object_id)
        
        # Prepare camera for update
        camera_for_update = Camera(
            id=None,  # Set to None to avoid ObjectId validation issues
            brand="Nikon",
            model="F3",
            year_manufactured=1980,
            type="SLR",
            film_format="35mm",
            condition="excellent",
            notes="Test notes"
        )
        
        # patch ObjectId to avoid validation issues
        with patch('bson.objectid.ObjectId', return_value=object_id):
            mock_result = AsyncMock()
            mock_result.matched_count = 1
            mock_db.cameras.update_one.return_value = mock_result
            
            # For the get_by_id call after update
            mock_db.cameras.find_one.return_value = {
                "_id": object_id,
                "brand": camera_for_update.brand,
                "model": camera_for_update.model,
                "year_manufactured": camera_for_update.year_manufactured,
                "type": camera_for_update.type,
                "film_format": camera_for_update.film_format,
                "condition": camera_for_update.condition,
                "notes": "Test notes"
            }
            
            # Call repository
            updated_camera = await camera_repo.update(camera_id, camera_for_update)
            
            # Assert
            mock_db.cameras.update_one.assert_called_once()
            assert updated_camera.id == camera_id
            assert updated_camera.notes == "Test notes"
    
    async def test_update_camera_not_found(self, camera_repo, mock_db, sample_camera):
        """Test updating a non-existent camera."""
        # Setup mock
        object_id = ObjectId()
        camera_id = str(object_id)
        
        # Prepare camera for update
        camera_for_update = Camera(
            id=None,  # Set to None to avoid ObjectId validation issues
            brand="Nikon",
            model="F3",
            year_manufactured=1980,
            type="SLR",
            film_format="35mm",
            condition="excellent"
        )
        
        # patch ObjectId to avoid validation issues
        with patch('bson.objectid.ObjectId', return_value=object_id):
            mock_result = AsyncMock()
            mock_result.matched_count = 0
            mock_db.cameras.update_one.return_value = mock_result
            
            # Assert
            with pytest.raises(NotFoundError):
                await camera_repo.update(camera_id, camera_for_update)
    
    async def test_delete_camera(self, camera_repo, mock_db):
        """Test deleting a camera."""
        # Setup mock
        object_id = ObjectId()
        camera_id = str(object_id)
        
        # patch ObjectId to avoid validation issues
        with patch('bson.objectid.ObjectId', return_value=object_id):
            mock_result = AsyncMock()
            mock_result.deleted_count = 1
            mock_db.cameras.delete_one.return_value = mock_result
            
            # Call repository
            result = await camera_repo.delete(camera_id)
            
            # Assert
            mock_db.cameras.delete_one.assert_called_once()
            assert result is True
    
    async def test_delete_camera_not_found(self, camera_repo, mock_db):
        """Test deleting a non-existent camera."""
        # Setup mock
        object_id = ObjectId()
        camera_id = str(object_id)
        
        # patch ObjectId to avoid validation issues
        with patch('bson.objectid.ObjectId', return_value=object_id):
            mock_result = AsyncMock()
            mock_result.deleted_count = 0
            mock_db.cameras.delete_one.return_value = mock_result
            
            # Assert
            with pytest.raises(NotFoundError):
                await camera_repo.delete(camera_id)
    
    async def test_get_stats_by_brand(self, camera_repo, mock_db):
        """Test getting camera statistics by brand."""
        # Setup mock
        mock_aggregation = [
            {"brand": "Nikon", "count": 5},
            {"brand": "Leica", "count": 3},
            {"brand": "Canon", "count": 2}
        ]
        
        mock_cursor = AsyncMock()
        mock_db.cameras.aggregate.return_value = mock_cursor
        mock_cursor.to_list.return_value = mock_aggregation
        
        # Call repository
        result = await camera_repo.get_stats_by_brand()
        
        # Assert
        mock_db.cameras.aggregate.assert_called_once()
        assert len(result) == 3
        assert result[0]["brand"] == "Nikon"
        assert result[0]["count"] == 5
    
    async def test_get_stats_by_type(self, camera_repo, mock_db):
        """Test getting camera statistics by type."""
        # Setup mock
        mock_aggregation = [
            {"type": "SLR", "count": 4},
            {"type": "rangefinder", "count": 3},
            {"type": "medium format", "count": 2}
        ]
        
        mock_cursor = AsyncMock()
        mock_db.cameras.aggregate.return_value = mock_cursor
        mock_cursor.to_list.return_value = mock_aggregation
        
        # Call repository
        result = await camera_repo.get_stats_by_type()
        
        # Assert
        mock_db.cameras.aggregate.assert_called_once()
        assert len(result) == 3
        assert result[0]["type"] == "SLR"
        assert result[0]["count"] == 4
    
    async def test_get_stats_by_decade(self, camera_repo, mock_db):
        """Test getting camera statistics by decade."""
        # Setup mock
        mock_aggregation = [
            {"decade": "1950s", "count": 2},
            {"decade": "1960s", "count": 1},
            {"decade": "1970s", "count": 3},
            {"decade": "1980s", "count": 4}
        ]
        
        mock_cursor = AsyncMock()
        mock_db.cameras.aggregate.return_value = mock_cursor
        mock_cursor.to_list.return_value = mock_aggregation
        
        # Call repository
        result = await camera_repo.get_stats_by_decade()
        
        # Assert
        mock_db.cameras.aggregate.assert_called_once()
        assert len(result) == 4
        assert result[0]["decade"] == "1950s"
        assert result[0]["count"] == 2
    
    async def test_get_total_value(self, camera_repo, mock_db):
        """Test getting total value of all cameras."""
        # Setup mock
        mock_aggregation = [{"total_value": 5000.0}]
        
        mock_cursor = AsyncMock()
        mock_db.cameras.aggregate.return_value = mock_cursor
        mock_cursor.to_list.return_value = mock_aggregation
        
        # Call repository
        result = await camera_repo.get_total_value()
        
        # Assert
        mock_db.cameras.aggregate.assert_called_once()
        assert result == 5000.0
        
    async def test_get_total_value_no_cameras(self, camera_repo, mock_db):
        """Test getting total value when there are no cameras."""
        # Setup mock
        mock_cursor = AsyncMock()
        mock_db.cameras.aggregate.return_value = mock_cursor
        mock_cursor.to_list.return_value = []
        
        # Call repository
        result = await camera_repo.get_total_value()
        
        # Assert
        mock_db.cameras.aggregate.assert_called_once()
        assert result == 0.0