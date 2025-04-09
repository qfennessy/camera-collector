from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from camera_collector.services.camera_service import CameraService
from camera_collector.api.dependencies import get_camera_service, get_current_user_id
from camera_collector.schemas.camera import BrandStats, TypeStats, DecadeStats, ValueStats
from camera_collector.core.exceptions import DatabaseError


router = APIRouter(
    prefix="/stats",
    tags=["statistics"],
    responses={
        401: {"description": "Unauthorized"},
        500: {"description": "Internal Server Error"},
    },
)


@router.get("/brands", response_model=List[BrandStats])
async def get_camera_stats_by_brand(
    camera_service: CameraService = Depends(get_camera_service),
    _: str = Depends(get_current_user_id),
):
    """Get camera statistics grouped by brand.
    
    Args:
        camera_service: Camera service dependency
        _: Current user ID for authentication
        
    Returns:
        List of brand statistics
    """
    try:
        return await camera_service.get_stats_by_brand()
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/types", response_model=List[TypeStats])
async def get_camera_stats_by_type(
    camera_service: CameraService = Depends(get_camera_service),
    _: str = Depends(get_current_user_id),
):
    """Get camera statistics grouped by type.
    
    Args:
        camera_service: Camera service dependency
        _: Current user ID for authentication
        
    Returns:
        List of type statistics
    """
    try:
        return await camera_service.get_stats_by_type()
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/decades", response_model=List[DecadeStats])
async def get_camera_stats_by_decade(
    camera_service: CameraService = Depends(get_camera_service),
    _: str = Depends(get_current_user_id),
):
    """Get camera statistics grouped by decade of manufacture.
    
    Args:
        camera_service: Camera service dependency
        _: Current user ID for authentication
        
    Returns:
        List of decade statistics
    """
    try:
        return await camera_service.get_stats_by_decade()
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/value", response_model=ValueStats)
async def get_total_value(
    camera_service: CameraService = Depends(get_camera_service),
    _: str = Depends(get_current_user_id),
):
    """Get total estimated value of all cameras.
    
    Args:
        camera_service: Camera service dependency
        _: Current user ID for authentication
        
    Returns:
        Total value statistics
    """
    try:
        return await camera_service.get_total_value()
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )