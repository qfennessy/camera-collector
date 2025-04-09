from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
import uuid


class CameraBase(BaseModel):
    """Base model for camera data."""
    brand: str
    model: str
    year_manufactured: int
    type: str  # e.g., SLR, TLR, rangefinder, etc.
    film_format: str  # e.g., 35mm, 120, 4x5, etc.
    condition: str  # e.g., mint, excellent, good, fair, poor
    special_features: Optional[List[str]] = []
    notes: Optional[str] = None
    acquisition_date: Optional[date] = None
    acquisition_price: Optional[float] = None
    estimated_value: Optional[float] = None
    images: Optional[List[str]] = []  # URLs to camera images


class CameraCreate(CameraBase):
    """Model for creating a new camera."""
    pass


class CameraUpdate(BaseModel):
    """Model for updating an existing camera."""
    brand: Optional[str] = None
    model: Optional[str] = None
    year_manufactured: Optional[int] = None
    type: Optional[str] = None
    film_format: Optional[str] = None
    condition: Optional[str] = None
    special_features: Optional[List[str]] = None
    notes: Optional[str] = None
    acquisition_date: Optional[date] = None
    acquisition_price: Optional[float] = None
    estimated_value: Optional[float] = None
    images: Optional[List[str]] = None


class Camera(CameraBase):
    """Full camera model with all fields."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "brand": "Nikon",
                "model": "F3",
                "year_manufactured": 1980,
                "type": "SLR",
                "film_format": "35mm",
                "condition": "excellent",
                "special_features": ["high-speed", "titanium shutter"],
                "notes": "Classic professional SLR",
                "acquisition_date": "2023-01-15",
                "acquisition_price": 450.00,
                "estimated_value": 500.00,
                "images": [],
                "created_at": "2023-01-15T12:00:00Z",
                "updated_at": "2023-01-15T12:00:00Z"
            }
        }