from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import JSONResponse

from camera_collector.services.camera_service import CameraService
from camera_collector.api.dependencies import get_camera_service, get_current_user_id
from camera_collector.schemas.camera import (
    CameraCreate, CameraUpdate, CameraResponse, CameraListResponse
)
from camera_collector.core.exceptions import NotFoundError, DatabaseError


router = APIRouter(
    prefix="/cameras",
    tags=["cameras"],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
    },
)


@router.get("", response_model=CameraListResponse)
async def get_cameras(
    skip: int = 0,
    limit: int = 10,
    brand: Optional[str] = None,
    type: Optional[str] = None,
    film_format: Optional[str] = None,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    condition: Optional[str] = None,
    camera_service: CameraService = Depends(get_camera_service),
    _: str = Depends(get_current_user_id),
):
    """Get all cameras with pagination and filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        brand: Filter by brand
        type: Filter by camera type
        film_format: Filter by film format
        year_min: Filter by minimum year of manufacture
        year_max: Filter by maximum year of manufacture
        condition: Filter by camera condition
        camera_service: Camera service dependency
        _: Current user ID for authentication
        
    Returns:
        List of cameras
    """
    try:
        return await camera_service.get_cameras(
            skip=skip,
            limit=limit,
            brand=brand,
            type=type,
            film_format=film_format,
            year_min=year_min,
            year_max=year_max,
            condition=condition,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
async def create_camera(
    camera_data: CameraCreate,
    camera_service: CameraService = Depends(get_camera_service),
    _: str = Depends(get_current_user_id),
):
    """Create a new camera.
    
    Args:
        camera_data: Camera data
        camera_service: Camera service dependency
        _: Current user ID for authentication
        
    Returns:
        Created camera
    """
    try:
        return await camera_service.create_camera(camera_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{camera_id}", response_model=CameraResponse)
async def get_camera(
    camera_id: str,
    camera_service: CameraService = Depends(get_camera_service),
    _: str = Depends(get_current_user_id),
):
    """Get camera by ID.
    
    Args:
        camera_id: Camera ID
        camera_service: Camera service dependency
        _: Current user ID for authentication
        
    Returns:
        Camera if found
    """
    try:
        return await camera_service.get_camera(camera_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put("/{camera_id}", response_model=CameraResponse)
async def update_camera(
    camera_id: str,
    camera_data: CameraUpdate,
    camera_service: CameraService = Depends(get_camera_service),
    _: str = Depends(get_current_user_id),
):
    """Update camera.
    
    Args:
        camera_id: Camera ID
        camera_data: Updated camera data
        camera_service: Camera service dependency
        _: Current user ID for authentication
        
    Returns:
        Updated camera
    """
    try:
        return await camera_service.update_camera(camera_id, camera_data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_camera(
    camera_id: str,
    camera_service: CameraService = Depends(get_camera_service),
    _: str = Depends(get_current_user_id),
):
    """Delete camera.
    
    Args:
        camera_id: Camera ID
        camera_service: Camera service dependency
        _: Current user ID for authentication
        
    Returns:
        No content if successful
    """
    try:
        deleted = await camera_service.delete_camera(camera_id)
        if deleted:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/{camera_id}/images", response_model=CameraResponse)
async def upload_image(
    camera_id: str,
    image: UploadFile = File(...),
    camera_service: CameraService = Depends(get_camera_service),
    _: str = Depends(get_current_user_id),
):
    """Upload a camera image.
    
    Args:
        camera_id: Camera ID
        image: Image file
        camera_service: Camera service dependency
        _: Current user ID for authentication
        
    Returns:
        Updated camera with new image URL
    """
    # In a real implementation, this would upload the image to a storage service
    # and add the URL to the camera's images list
    
    # For now, we'll just return a mock image URL
    try:
        # Get existing camera
        camera = await camera_service.get_camera(camera_id)
        
        # Add mock image URL (in a real app, we would upload to storage)
        image_url = f"/static/images/{camera_id}/{image.filename}"
        
        # Update camera with new image URL
        camera_data = CameraUpdate(
            images=[*camera.images, image_url]
        )
        
        return await camera_service.update_camera(camera_id, camera_data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )