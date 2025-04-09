#!/usr/bin/env python3
"""
Seed script to populate the database with initial test data.
"""
import asyncio
import sys
import os
import json
from datetime import datetime, date

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from motor.motor_asyncio import AsyncIOMotorClient
from camera_collector.core.config import settings
from camera_collector.models.camera import Camera


# Sample camera data
SAMPLE_CAMERAS = [
    {
        "brand": "Nikon",
        "model": "F3",
        "year_manufactured": 1980,
        "type": "SLR",
        "film_format": "35mm",
        "condition": "excellent",
        "special_features": ["high-speed", "titanium shutter"],
        "notes": "Professional model used by photojournalists",
        "acquisition_date": "2022-01-15",
        "acquisition_price": 450.00,
        "estimated_value": 500.00,
        "images": []
    },
    {
        "brand": "Leica",
        "model": "M3",
        "year_manufactured": 1954,
        "type": "rangefinder",
        "film_format": "35mm",
        "condition": "good",
        "special_features": ["double stroke", "original viewfinder"],
        "notes": "Classic rangefinder camera",
        "acquisition_date": "2021-11-20",
        "acquisition_price": 1200.00,
        "estimated_value": 1500.00,
        "images": []
    },
    {
        "brand": "Hasselblad",
        "model": "500C/M",
        "year_manufactured": 1970,
        "type": "medium format",
        "film_format": "120",
        "condition": "mint",
        "special_features": ["waist-level finder", "interchangeable backs"],
        "notes": "Swedish medium format camera",
        "acquisition_date": "2022-03-10",
        "acquisition_price": 900.00,
        "estimated_value": 1200.00,
        "images": []
    }
]


async def seed_cameras(db):
    """Seed the cameras collection with sample data."""
    print("Seeding cameras collection...")
    
    # Process dates from string to date objects
    for camera in SAMPLE_CAMERAS:
        if "acquisition_date" in camera and isinstance(camera["acquisition_date"], str):
            camera["acquisition_date"] = date.fromisoformat(camera["acquisition_date"])
    
    # Insert all cameras
    result = await db.cameras.insert_many(SAMPLE_CAMERAS)
    print(f"Added {len(result.inserted_ids)} cameras to the database.")


async def main():
    """Main seed function."""
    print(f"Connecting to MongoDB at {settings.MONGODB_URL}...")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB]
    
    # Clear existing data
    await db.cameras.delete_many({})
    print("Cleared existing camera data.")
    
    await seed_cameras(db)
    
    # Close connection
    client.close()
    print("Database seeding completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())