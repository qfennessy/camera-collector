from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime, date


class CameraBase(BaseModel):
    """Base camera schema with common attributes."""
    brand: str
    model: str
    year_manufactured: int
    type: str
    film_format: str
    condition: str
    special_features: Optional[List[str]] = []
    notes: Optional[str] = None
    acquisition_date: Optional[date] = None
    acquisition_price: Optional[float] = None
    estimated_value: Optional[float] = None
    images: Optional[List[str]] = []
    
    @validator("year_manufactured")
    def validate_year(cls, v):
        """Validate the year of manufacture."""
        current_year = datetime.now().year
        if v < 1800 or v > current_year:
            raise ValueError(f"Year must be between 1800 and {current_year}")
        return v
    
    @validator("condition")
    def validate_condition(cls, v):
        """Validate the condition value."""
        valid_conditions = ["mint", "excellent", "very good", "good", "fair", "poor"]
        if v.lower() not in valid_conditions:
            raise ValueError(f"Condition must be one of: {', '.join(valid_conditions)}")
        return v.lower()


class CameraCreate(CameraBase):
    """Schema for creating a camera."""
    pass


class CameraUpdate(BaseModel):
    """Schema for updating a camera."""
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
    
    @validator("year_manufactured")
    def validate_year(cls, v):
        """Validate the year of manufacture."""
        if v is None:
            return v
        current_year = datetime.now().year
        if v < 1800 or v > current_year:
            raise ValueError(f"Year must be between 1800 and {current_year}")
        return v
    
    @validator("condition")
    def validate_condition(cls, v):
        """Validate the condition value."""
        if v is None:
            return v
        valid_conditions = ["mint", "excellent", "very good", "good", "fair", "poor"]
        if v.lower() not in valid_conditions:
            raise ValueError(f"Condition must be one of: {', '.join(valid_conditions)}")
        return v.lower()


class CameraInDB(CameraBase):
    """Schema for camera data in the database."""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class CameraResponse(CameraInDB):
    """Schema for camera data in responses."""
    pass


class CameraListResponse(BaseModel):
    """Schema for paginated camera list response."""
    items: List[CameraResponse]
    total: int
    page: int
    size: int
    pages: int


class BrandStats(BaseModel):
    """Schema for brand statistics."""
    brand: str
    count: int


class TypeStats(BaseModel):
    """Schema for type statistics."""
    type: str
    count: int


class DecadeStats(BaseModel):
    """Schema for decade statistics."""
    decade: str
    count: int


class ValueStats(BaseModel):
    """Schema for value statistics."""
    total_value: float