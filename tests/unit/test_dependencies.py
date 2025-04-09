import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from jose import JWTError

from camera_collector.api.dependencies import (
    get_camera_repository,
    get_camera_service,
    get_auth_service,
    get_current_user_id
)
from camera_collector.db.repositories.camera_repository import CameraRepository
from camera_collector.db.repositories.user_repository import UserRepository
from camera_collector.services.camera_service import CameraService
from camera_collector.services.auth_service import AuthService
from camera_collector.core.exceptions import AuthenticationError


@pytest.mark.asyncio
class TestDependencies:
    """Test API dependencies."""
    
    @pytest.fixture
    def mock_db(self):
        """Mock database fixture."""
        return MagicMock()
    
    async def test_get_camera_repository(self, mock_db):
        """Test get_camera_repository dependency."""
        repo = await get_camera_repository(mock_db)
        assert isinstance(repo, CameraRepository)
        assert repo.db == mock_db
    
    async def test_get_camera_service(self):
        """Test get_camera_service dependency."""
        # Setup mocks
        mock_camera_repo = MagicMock(spec=CameraRepository)
        
        # Call the dependency function
        service = await get_camera_service(mock_camera_repo)
        
        # Verify result
        assert isinstance(service, CameraService)
        assert service.repository == mock_camera_repo
    
    async def test_get_auth_service(self):
        """Test get_auth_service dependency."""
        # Setup mocks
        mock_user_repo = MagicMock(spec=UserRepository)
        
        # Call the dependency function
        service = await get_auth_service(mock_user_repo)
        
        # Verify result
        assert isinstance(service, AuthService)
        assert service.user_repository == mock_user_repo
    
    async def test_get_current_user_id(self):
        """Test get_current_user_id dependency."""
        # Create a mock user dict
        mock_current_user = {"id": "test_user_id"}
        
        # Call the dependency function
        result = await get_current_user_id(mock_current_user)
        
        # Verify result
        assert result == "test_user_id"