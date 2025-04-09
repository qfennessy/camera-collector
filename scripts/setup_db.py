#!/usr/bin/env python3
"""
Database setup script.
Creates indexes and initial data in MongoDB.
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from motor.motor_asyncio import AsyncIOMotorClient
from camera_collector.core.config import settings


async def setup_indexes(db):
    """Create MongoDB indexes for performance."""
    print("Creating indexes...")
    
    # Camera collection indexes
    await db.cameras.create_index("brand")
    await db.cameras.create_index("type")
    await db.cameras.create_index("year_manufactured")
    await db.cameras.create_index("film_format")
    
    # User collection indexes
    await db.users.create_index("email", unique=True)
    await db.users.create_index("username", unique=True)
    
    print("Indexes created successfully.")


async def main():
    """Main setup function."""
    print(f"Connecting to MongoDB at {settings.MONGODB_URL}...")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB]
    
    await setup_indexes(db)
    
    # Close connection
    client.close()
    print("Database setup completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())