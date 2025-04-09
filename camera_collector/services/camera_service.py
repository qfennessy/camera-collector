from typing import List, Optional, Dict, Any
from datetime import datetime

from camera_collector.db.repositories.camera_repository import CameraRepository
from camera_collector.models.camera import Camera
from camera_collector.schemas.camera import (
    CameraCreate, CameraUpdate, CameraResponse, CameraListResponse,
    BrandStats, TypeStats, DecadeStats, ValueStats
)


class CameraService:
    """Business logic for camera operations."""
    
    def __init__(self, repository: CameraRepository):
        self.repository = repository
    
    async def create_camera(self, camera_data: CameraCreate) -> CameraResponse:
        """Create a new camera.
        
        Args:
            camera_data: Camera data
            
        Returns:
            Created camera
        """
        # Create Camera model from schema
        camera = Camera(
            **camera_data.dict(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Save to database
        created_camera = await self.repository.create(camera)
        return CameraResponse.from_orm(created_camera)
    
    async def get_camera(self, camera_id: str) -> CameraResponse:
        """Get a camera by ID.
        
        Args:
            camera_id: Camera ID
            
        Returns:
            Camera if found
        """
        camera = await self.repository.get_by_id(camera_id)
        return CameraResponse.from_orm(camera)
    
    async def get_cameras(
        self, 
        skip: int = 0, 
        limit: int = 10,
        brand: Optional[str] = None,
        type: Optional[str] = None,
        film_format: Optional[str] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        condition: Optional[str] = None
    ) -> CameraListResponse:
        """Get cameras with pagination and filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            brand: Filter by brand
            type: Filter by type
            film_format: Filter by film format
            year_min: Filter by minimum year
            year_max: Filter by maximum year
            condition: Filter by condition
            
        Returns:
            List of cameras
        """
        # Build filters
        filters = {}
        if brand:
            filters["brand"] = brand
        if type:
            filters["type"] = type
        if film_format:
            filters["film_format"] = film_format
        if condition:
            filters["condition"] = condition
        
        # Year range filter
        if year_min or year_max:
            filters["year_manufactured"] = {}
            if year_min:
                filters["year_manufactured"]["$gte"] = year_min
            if year_max:
                filters["year_manufactured"]["$lte"] = year_max
        
        # Get cameras and total count
        cameras = await self.repository.get_all(skip=skip, limit=limit, filters=filters)
        total = await self.repository.count(filters=filters)
        
        # Calculate pagination data
        page = skip // limit + 1 if limit > 0 else 1
        total_pages = (total + limit - 1) // limit if limit > 0 else 1
        
        # Map to response model
        camera_responses = [CameraResponse.from_orm(camera) for camera in cameras]
        
        return CameraListResponse(
            items=camera_responses,
            total=total,
            page=page,
            size=limit,
            pages=total_pages
        )
    
    async def update_camera(self, camera_id: str, camera_data: CameraUpdate) -> CameraResponse:
        """Update a camera.
        
        Args:
            camera_id: Camera ID
            camera_data: Updated camera data
            
        Returns:
            Updated camera
        """
        # Get existing camera to merge with update data
        existing_camera = await self.repository.get_by_id(camera_id)
        
        # Merge existing data with update data (including None values)
        update_dict = camera_data.dict(exclude_unset=True)
        
        # Add updated_at timestamp
        update_dict["updated_at"] = datetime.now()
        
        # Create merged Camera model
        camera_model = Camera(**{**existing_camera.dict(), **update_dict})
        
        # Update in database
        updated_camera = await self.repository.update(camera_id, camera_model)
        return CameraResponse.from_orm(updated_camera)
    
    async def delete_camera(self, camera_id: str) -> bool:
        """Delete a camera.
        
        Args:
            camera_id: Camera ID
            
        Returns:
            True if camera was deleted
        """
        return await self.repository.delete(camera_id)
    
    async def get_stats_by_brand(self) -> List[BrandStats]:
        """Get camera statistics by brand.
        
        Returns:
            Brand statistics
        """
        stats = await self.repository.get_stats_by_brand()
        return [BrandStats(**stat) for stat in stats]
    
    async def get_stats_by_type(self) -> List[TypeStats]:
        """Get camera statistics by type.
        
        Returns:
            Type statistics
        """
        stats = await self.repository.get_stats_by_type()
        return [TypeStats(**stat) for stat in stats]
    
    async def get_stats_by_decade(self) -> List[DecadeStats]:
        """Get camera statistics by decade.
        
        Returns:
            Decade statistics
        """
        stats = await self.repository.get_stats_by_decade()
        return [DecadeStats(**stat) for stat in stats]
    
    async def get_total_value(self) -> ValueStats:
        """Get total value of all cameras.
        
        Returns:
            Total value statistics
        """
        total_value = await self.repository.get_total_value()
        return ValueStats(total_value=total_value)