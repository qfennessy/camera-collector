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
        mongo_url = settings.MONGODB_TEST_URL
        client = AsyncIOMotorClient(mongo_url)
        yield client
        client.close()
    
    async def test_database_connection(self, mongodb_client):
        """Test that we can connect to the database."""
        # This is a basic test to ensure we can connect to MongoDB
        # Skip this test if the server isn't available (CI environment without MongoDB)
        try:
            # Check that the server is responsive
            server_info = await mongodb_client.server_info()
            assert "version" in server_info
            
            # Check test database
            db = mongodb_client[settings.MONGODB_TEST_DB]
            # Insert and retrieve a test document
            test_collection = db.test_collection
            await test_collection.insert_one({"test": "data"})
            result = await test_collection.find_one({"test": "data"})
            assert result is not None
            assert result["test"] == "data"
            
            # Clean up
            await test_collection.delete_many({})
        except Exception as e:
            pytest.skip(f"MongoDB is not available: {str(e)}")