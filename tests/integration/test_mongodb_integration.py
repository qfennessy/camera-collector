import pytest
import pytest_asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from camera_collector.core.config import settings
from camera_collector.models.camera import Camera, CameraCreate


@pytest.mark.integration
@pytest.mark.asyncio
class TestMongoDBIntegration:
    """Test integration with MongoDB."""
    
    @pytest_asyncio.fixture
    async def mongo_client(self):
        """Create a MongoDB client for testing."""
        # Check if we're running in Docker test environment
        if os.environ.get("ENVIRONMENT") == "test":
            host = "mongodb_test"
            port = 27017
        else:
            host = "localhost"
            port = 27017
            
        # Use test database settings
        mongo_url = f"mongodb://{host}:{port}"
        client = AsyncIOMotorClient(mongo_url)
        
        # Create a test database
        db = client.camera_collector_test
        
        # Clean up before tests
        await db.cameras.delete_many({})
        
        yield db
        
        # Clean up after tests
        await db.cameras.delete_many({})
        client.close()
    
    @pytest.mark.skip("Skipping MongoDB connection test as requested")
    async def test_mongo_connection(self, mongo_client):
        """Test that we can connect to MongoDB."""
        # Check that the server is responsive
        server_info = await mongo_client.client.server_info()
        assert "version" in server_info
    
    async def test_camera_crud_operations(self, mongo_client):
        """Test CRUD operations on the cameras collection."""
        # Create a test camera
        camera_data = {
            "brand": "Test Brand",
            "model": "Test Model",
            "year_manufactured": 2020,
            "type": "SLR",
            "film_format": "35mm",
            "condition": "excellent",
            "special_features": ["test feature"],
            "notes": "Test notes",
        }
        
        # 1. CREATE: Insert the camera
        result = await mongo_client.cameras.insert_one(camera_data)
        assert result.inserted_id is not None
        camera_id = result.inserted_id
        
        # 2. READ: Get the camera
        camera = await mongo_client.cameras.find_one({"_id": camera_id})
        assert camera is not None
        assert camera["brand"] == "Test Brand"
        assert camera["model"] == "Test Model"
        
        # 3. UPDATE: Update the camera
        update_result = await mongo_client.cameras.update_one(
            {"_id": camera_id},
            {"$set": {"condition": "mint"}}
        )
        assert update_result.modified_count == 1
        
        # Verify the update
        updated_camera = await mongo_client.cameras.find_one({"_id": camera_id})
        assert updated_camera["condition"] == "mint"
        
        # 4. DELETE: Delete the camera
        delete_result = await mongo_client.cameras.delete_one({"_id": camera_id})
        assert delete_result.deleted_count == 1
        
        # Verify deletion
        deleted_camera = await mongo_client.cameras.find_one({"_id": camera_id})
        assert deleted_camera is None
    
    async def test_camera_query_operations(self, mongo_client):
        """Test query operations on the cameras collection."""
        # Insert multiple cameras
        cameras = [
            {
                "brand": "Nikon",
                "model": "F3",
                "year_manufactured": 1980,
                "type": "SLR",
                "film_format": "35mm",
                "condition": "excellent",
            },
            {
                "brand": "Canon",
                "model": "AE-1",
                "year_manufactured": 1976,
                "type": "SLR",
                "film_format": "35mm",
                "condition": "good",
            },
            {
                "brand": "Leica",
                "model": "M3",
                "year_manufactured": 1954,
                "type": "rangefinder",
                "film_format": "35mm",
                "condition": "mint",
            }
        ]
        
        await mongo_client.cameras.insert_many(cameras)
        
        # Test simple query
        nikon_cameras = await mongo_client.cameras.find({"brand": "Nikon"}).to_list(length=10)
        assert len(nikon_cameras) == 1
        assert nikon_cameras[0]["model"] == "F3"
        
        # Test query with multiple conditions
        slr_cameras = await mongo_client.cameras.find({
            "type": "SLR",
            "film_format": "35mm"
        }).to_list(length=10)
        assert len(slr_cameras) == 2
        
        # Test query with operators
        old_cameras = await mongo_client.cameras.find({
            "year_manufactured": {"$lt": 1970}
        }).to_list(length=10)
        assert len(old_cameras) == 1
        assert old_cameras[0]["brand"] == "Leica"
        
        # Test sorting
        sorted_cameras = await mongo_client.cameras.find().sort("year_manufactured", 1).to_list(length=10)
        assert sorted_cameras[0]["brand"] == "Leica"
        assert sorted_cameras[-1]["brand"] == "Nikon"
        
        # Test projection
        brands_only = await mongo_client.cameras.find({}, {"brand": 1, "_id": 0}).to_list(length=10)
        assert len(brands_only) == 3
        assert "brand" in brands_only[0]
        assert "model" not in brands_only[0]