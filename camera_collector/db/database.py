from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from camera_collector.core.config import settings


class Database:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


db = Database()


async def connect_to_mongodb():
    """Connect to MongoDB."""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.db = db.client[settings.MONGODB_DB]
    print(f"Connected to MongoDB at {settings.MONGODB_URL}")


async def close_mongodb_connection():
    """Close MongoDB connection."""
    if db.client:
        db.client.close()
        print("Closed MongoDB connection")