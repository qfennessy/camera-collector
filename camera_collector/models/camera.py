from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
import uuid


class Camera(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    brand: str
    model: str
    year_manufactured: int
    type: str  # e.g., SLR, TLR, rangefinder, etc.
    film_format: str  # e.g., 35mm, 120, 4x5, etc.
    condition: str  # e.g., mint, excellent, good, fair, poor
    special_features: List[str] = []
    notes: Optional[str] = None
    acquisition_date: Optional[date] = None
    acquisition_price: Optional[float] = None
    estimated_value: Optional[float] = None
    images: List[str] = []  # URLs to camera images
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)