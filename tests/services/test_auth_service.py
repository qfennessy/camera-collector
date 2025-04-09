import pytest
from unittest.mock import AsyncMock, patch
import pytest_asyncio

from camera_collector.services.auth_service import AuthService
from camera_collector.schemas.user import UserCreate
from camera_collector.models.user import User
from camera_collector.core.exceptions import AuthenticationError, ValidationError


@pytest.mark.asyncio
class TestAuthService:
    """Test authentication service."""
    
    @pytest_asyncio.fixture
    async def mock_user_repo(self):
        """Mock user repository fixture."""
        repository = AsyncMock()
        return repository
    
    @pytest_asyncio.fixture
    async def auth_service(self, mock_user_repo):
        """Auth service fixture."""
        return AuthService(mock_user_repo)
    
    @pytest_asyncio.fixture
    async def sample_user_data(self):
        """Sample user data fixture."""
        return UserCreate(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
    
    async def test_register_user(self, auth_service, mock_user_repo, sample_user_data):
        """Test registering a new user."""
        # Setup mocks
        mock_user_repo.get_by_username.return_value = None
        mock_user_repo.get_by_email.return_value = None
        
        created_user = User(
            id="123",
            username=sample_user_data.username,
            email=sample_user_data.email,
            hashed_password="hashed_password"
        )
        mock_user_repo.create.return_value = created_user
        
        # Call service
        with patch("camera_collector.services.auth_service.get_password_hash", return_value="hashed_password"):
            result = await auth_service.register_user(sample_user_data)
        
        # Assert
        mock_user_repo.get_by_username.assert_called_once_with(sample_user_data.username)
        mock_user_repo.get_by_email.assert_called_once_with(sample_user_data.email)
        mock_user_repo.create.assert_called_once()
        assert result.username == sample_user_data.username
        assert result.email == sample_user_data.email
    
    async def test_register_user_username_exists(self, auth_service, mock_user_repo, sample_user_data):
        """Test registering a user with existing username."""
        # Setup mock
        existing_user = User(
            id="123",
            username=sample_user_data.username,
            email="other@example.com",
            hashed_password="hashed_password"
        )
        mock_user_repo.get_by_username.return_value = existing_user
        
        # Assert
        with pytest.raises(ValidationError, match="Username already registered"):
            await auth_service.register_user(sample_user_data)
    
    async def test_register_user_email_exists(self, auth_service, mock_user_repo, sample_user_data):
        """Test registering a user with existing email."""
        # Setup mocks
        mock_user_repo.get_by_username.return_value = None
        
        existing_user = User(
            id="123",
            username="otheruser",
            email=sample_user_data.email,
            hashed_password="hashed_password"
        )
        mock_user_repo.get_by_email.return_value = existing_user
        
        # Assert
        with pytest.raises(ValidationError, match="Email already registered"):
            await auth_service.register_user(sample_user_data)
    
    async def test_authenticate_user_success(self, auth_service, mock_user_repo):
        """Test successful user authentication."""
        # Setup mocks
        username = "testuser"
        password = "password123"
        
        user = User(
            id="123",
            username=username,
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=True
        )
        mock_user_repo.get_by_username.return_value = user
        
        # Call service
        with patch("camera_collector.services.auth_service.verify_password", return_value=True):
            result = await auth_service.authenticate_user(username, password)
        
        # Assert
        mock_user_repo.get_by_username.assert_called_once_with(username)
        assert result.id == user.id
        assert result.username == username
    
    async def test_authenticate_user_not_found(self, auth_service, mock_user_repo):
        """Test authentication with non-existent user."""
        # Setup mock
        username = "testuser"
        password = "password123"
        mock_user_repo.get_by_username.return_value = None
        
        # Assert
        with pytest.raises(AuthenticationError, match="Invalid username or password"):
            await auth_service.authenticate_user(username, password)
    
    async def test_authenticate_user_wrong_password(self, auth_service, mock_user_repo):
        """Test authentication with wrong password."""
        # Setup mocks
        username = "testuser"
        password = "password123"
        
        user = User(
            id="123",
            username=username,
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=True
        )
        mock_user_repo.get_by_username.return_value = user
        
        # Call service
        with patch("camera_collector.services.auth_service.verify_password", return_value=False):
            with pytest.raises(AuthenticationError, match="Invalid username or password"):
                await auth_service.authenticate_user(username, password)
    
    async def test_authenticate_user_inactive(self, auth_service, mock_user_repo):
        """Test authentication with inactive user."""
        # Setup mocks
        username = "testuser"
        password = "password123"
        
        user = User(
            id="123",
            username=username,
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=False
        )
        mock_user_repo.get_by_username.return_value = user
        
        # Call service
        with patch("camera_collector.services.auth_service.verify_password", return_value=True):
            with pytest.raises(AuthenticationError, match="User account is inactive"):
                await auth_service.authenticate_user(username, password)
    
    async def test_login(self, auth_service, mock_user_repo):
        """Test login and token generation."""
        # Setup mocks
        username = "testuser"
        password = "password123"
        
        user = User(
            id="123",
            username=username,
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=True
        )
        
        # Call service
        with patch.object(auth_service, "authenticate_user", return_value=user) as mock_auth:
            with patch("camera_collector.services.auth_service.create_access_token", return_value="access_token"):
                with patch("camera_collector.services.auth_service.create_refresh_token", return_value="refresh_token"):
                    result = await auth_service.login(username, password)
        
        # Assert
        mock_auth.assert_called_once_with(username, password)
        assert result.access_token == "access_token"
        assert result.refresh_token == "refresh_token"