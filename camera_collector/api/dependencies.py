from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from camera_collector.db.database import db
from camera_collector.db.repositories.camera_repository import CameraRepository
from camera_collector.db.repositories.user_repository import UserRepository
from camera_collector.services.camera_service import CameraService
from camera_collector.services.auth_service import AuthService
from camera_collector.core.security import get_current_user


async def get_db() -> AsyncIOMotorDatabase:
    """Get database connection.
    
    Returns:
        Database connection
    """
    return db.db


async def get_camera_repository(database: AsyncIOMotorDatabase = Depends(get_db)) -> CameraRepository:
    """Get camera repository.
    
    Args:
        database: Database connection
        
    Returns:
        Camera repository
    """
    return CameraRepository(database)


async def get_user_repository(database: AsyncIOMotorDatabase = Depends(get_db)) -> UserRepository:
    """Get user repository.
    
    Args:
        database: Database connection
        
    Returns:
        User repository
    """
    return UserRepository(database)


async def get_camera_service(
    repository: CameraRepository = Depends(get_camera_repository),
) -> CameraService:
    """Get camera service.
    
    Args:
        repository: Camera repository
        
    Returns:
        Camera service
    """
    return CameraService(repository)


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    """Get authentication service.
    
    Args:
        user_repository: User repository
        
    Returns:
        Auth service
    """
    return AuthService(user_repository)


async def get_current_user_id(
    current_user = Depends(get_current_user)
) -> str:
    """Get current user ID from token.
    
    Args:
        current_user: Current user from token
        
    Returns:
        User ID
    """
    return current_user["id"]