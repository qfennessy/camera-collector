import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from camera_collector.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mongodb():
    """Create a MongoDB test database."""
    mongo_url = settings.MONGODB_TEST_URL
    mongo_db = settings.MONGODB_TEST_DB
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[mongo_db]
    
    # Return the database object directly
    yield db
    
    # Clean up
    await client.drop_database(mongo_db)
    client.close()