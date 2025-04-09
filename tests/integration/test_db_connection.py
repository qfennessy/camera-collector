import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os

from camera_collector.core.config import settings


# This test is marked as integration because it requires a real MongoDB instance
@pytest.mark.integration
@pytest.mark.asyncio
class TestDatabaseConnection:
    """Test MongoDB connection."""
    
    @pytest_asyncio.fixture
    async def mongodb_client(self):
        """MongoDB client fixture."""
        # Use test database settings
        mongo_url = os.environ.get("MONGODB_TEST_URL", settings.MONGODB_TEST_URL)
        client = AsyncIOMotorClient(mongo_url)
        yield client
        client.close()
    
    async def test_database_connection(self, mongodb_client, mongodb_available):
        """Test that we can connect to the database."""
        # Skip this test if MongoDB is not available
        if not mongodb_available:
            pytest.skip("MongoDB is not available")
            
        # Check that the server is responsive
        server_info = await mongodb_client.server_info()
        assert "version" in server_info
        
        # Check test database
        mongo_db = os.environ.get("MONGODB_TEST_DB", settings.MONGODB_TEST_DB)
        db = mongodb_client[mongo_db]
        
        # Insert and retrieve a test document
        test_collection = db.test_collection
        await test_collection.insert_one({"test": "data"})
        result = await test_collection.find_one({"test": "data"})
        assert result is not None
        assert result["test"] == "data"
        
        # Clean up
        await test_collection.delete_many({})
    
    async def test_collection_operations(self, mongodb_client, mongodb_available):
        """Test basic collection operations."""
        # Skip this test if MongoDB is not available
        if not mongodb_available:
            pytest.skip("MongoDB is not available")
            
        # Get the test database
        mongo_db = os.environ.get("MONGODB_TEST_DB", settings.MONGODB_TEST_DB)
        db = mongodb_client[mongo_db]
            
        # Insert a document
        await db.cameras.insert_one({
            "brand": "Test Brand",
            "model": "Test Model",
            "year_manufactured": 2020,
            "type": "SLR",
            "film_format": "35mm",
            "condition": "excellent"
        })
        
        # Find the document
        result = await db.cameras.find_one({"brand": "Test Brand"})
        assert result is not None
        assert result["model"] == "Test Model"
        
        # Update the document
        await db.cameras.update_one(
            {"brand": "Test Brand"},
            {"$set": {"condition": "mint"}}
        )
        
        # Verify the update
        updated = await db.cameras.find_one({"brand": "Test Brand"})
        assert updated["condition"] == "mint"
        
        # Delete the document
        await db.cameras.delete_one({"brand": "Test Brand"})
        
        # Verify deletion
        deleted = await db.cameras.find_one({"brand": "Test Brand"})
        assert deleted is None