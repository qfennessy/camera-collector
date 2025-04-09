import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import Generator, Any, Optional
from unittest.mock import AsyncMock, MagicMock
import socket
from camera_collector.core.config import settings


# Check if MongoDB is available
def is_mongodb_available(host: str = "localhost", port: int = 27017) -> bool:
    """Check if MongoDB is available on the given host and port."""
    try:
        # Check if we're running in Docker test environment
        if os.environ.get("ENVIRONMENT") == "test":
            host = "mongodb_test"
            port = 27017
        
        # Try to connect to the MongoDB server
        socket.create_connection((host, port), timeout=1)
        return True
    except (socket.timeout, socket.error):
        return False


# Determine if we should use real MongoDB
USE_REAL_MONGODB = is_mongodb_available()
if USE_REAL_MONGODB:
    print("Using real MongoDB for tests")
else:
    print("MongoDB not available, using mocks")


# Define pytest hooks
def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption(
        "--with-mongodb",
        action="store_true",
        default=False,
        help="Run tests with a real MongoDB instance"
    )

def pytest_configure(config):
    """Register markers."""
    config.addinivalue_line("markers", "mongodb: mark test as requiring MongoDB")


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mongodb():
    """
    Create a MongoDB test database if available, otherwise return a mock.
    
    This fixture will attempt to connect to a real MongoDB instance. If one is
    available, it will use that. Otherwise, it will return a mocked database.
    """
    if not USE_REAL_MONGODB:
        # Return a mocked database
        mock_db = AsyncMock()
        mock_db.cameras = AsyncMock()
        mock_db.users = AsyncMock()
        yield mock_db
        return
    
    # Use real MongoDB
    mongo_url = os.environ.get("MONGODB_TEST_URL", settings.MONGODB_TEST_URL)
    mongo_db = os.environ.get("MONGODB_TEST_DB", settings.MONGODB_TEST_DB)
    
    # Create a real client
    client = AsyncIOMotorClient(mongo_url)
    db = client[mongo_db]
    
    # Clear collections before tests
    await db.cameras.delete_many({})
    await db.users.delete_many({})
    
    # Yield the database object
    yield db
    
    # Clean up after tests
    await db.cameras.delete_many({})
    await db.users.delete_many({})
    client.close()


@pytest.fixture(scope="class")
def mongodb_available() -> bool:
    """
    Fixture to check if MongoDB is available.
    
    This can be used in tests to skip integration tests when MongoDB is not available.
    """
    return USE_REAL_MONGODB