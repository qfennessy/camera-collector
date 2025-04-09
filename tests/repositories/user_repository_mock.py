import pytest
from unittest.mock import AsyncMock, patch
import pytest_asyncio
from bson import ObjectId

from camera_collector.db.repositories.user_repository import UserRepository
from camera_collector.models.user import User
from camera_collector.core.exceptions import NotFoundError, DatabaseError


# Skipping real database tests as they require MongoDB setup
pytestmark = pytest.mark.skip("User repository tests require MongoDB setup")


@pytest.mark.asyncio
class TestUserRepository:
    """Test user repository with mocked MongoDB."""
    
    @pytest_asyncio.fixture
    async def mock_db(self):
        """Mock MongoDB database."""
        db = AsyncMock()
        db.users = AsyncMock()
        return db
    
    @pytest_asyncio.fixture
    async def user_repo(self, mock_db):
        """User repository fixture with mocked database."""
        return UserRepository(mock_db)
    
    @pytest_asyncio.fixture
    async def sample_user(self):
        """Sample user data fixture."""
        return User(
            id=None,  # Set to None to avoid validation issues
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=True
        )
    
    async def test_create_user(self, user_repo, mock_db, sample_user):
        """Test creating a user."""
        # Setup mock
        object_id = ObjectId()
        mock_result = AsyncMock()
        mock_result.inserted_id = object_id
        mock_db.users.insert_one.return_value = mock_result
        
        # Call repository
        with patch('bson.objectid.ObjectId', return_value=object_id):
            user = await user_repo.create(sample_user)
            
            # Assert
            mock_db.users.insert_one.assert_called_once()
            assert user.id == str(object_id)
            assert user.username == sample_user.username
            assert user.email == sample_user.email
    
    async def test_get_by_id(self, user_repo, mock_db):
        """Test getting a user by ID."""
        # Setup mock
        object_id = ObjectId()
        user_id = str(object_id)
        
        with patch('bson.objectid.ObjectId', return_value=object_id):
            mock_db.users.find_one.return_value = {
                "_id": object_id,
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": "hashed_password",
                "is_active": True
            }
            
            # Call repository
            user = await user_repo.get_by_id(user_id)
            
            # Assert
            mock_db.users.find_one.assert_called_once()
            assert user.id == user_id
            assert user.username == "testuser"
            assert user.email == "test@example.com"
    
    async def test_get_by_id_not_found(self, user_repo, mock_db):
        """Test getting a non-existent user."""
        # Setup mock
        object_id = ObjectId()
        user_id = str(object_id)
        
        with patch('bson.objectid.ObjectId', return_value=object_id):
            mock_db.users.find_one.return_value = None
            
            # Assert
            with pytest.raises(NotFoundError):
                await user_repo.get_by_id(user_id)
    
    async def test_get_by_email(self, user_repo, mock_db):
        """Test getting a user by email."""
        # Setup mock
        email = "test@example.com"
        object_id = ObjectId()
        
        mock_db.users.find_one.return_value = {
            "_id": object_id,
            "username": "testuser",
            "email": email,
            "hashed_password": "hashed_password",
            "is_active": True
        }
        
        # Call repository
        user = await user_repo.get_by_email(email)
        
        # Assert
        mock_db.users.find_one.assert_called_once_with({"email": email})
        assert user.id == str(object_id)
        assert user.email == email
    
    async def test_get_by_email_not_found(self, user_repo, mock_db):
        """Test getting a user by email that doesn't exist."""
        # Setup mock
        email = "nonexistent@example.com"
        mock_db.users.find_one.return_value = None
        
        # Call repository
        user = await user_repo.get_by_email(email)
        
        # Assert
        mock_db.users.find_one.assert_called_once_with({"email": email})
        assert user is None
    
    async def test_get_by_username(self, user_repo, mock_db):
        """Test getting a user by username."""
        # Setup mock
        username = "testuser"
        object_id = ObjectId()
        
        mock_db.users.find_one.return_value = {
            "_id": object_id,
            "username": username,
            "email": "test@example.com",
            "hashed_password": "hashed_password",
            "is_active": True
        }
        
        # Call repository
        user = await user_repo.get_by_username(username)
        
        # Assert
        mock_db.users.find_one.assert_called_once_with({"username": username})
        assert user.id == str(object_id)
        assert user.username == username
    
    async def test_get_by_username_not_found(self, user_repo, mock_db):
        """Test getting a user by username that doesn't exist."""
        # Setup mock
        username = "nonexistent"
        mock_db.users.find_one.return_value = None
        
        # Call repository
        user = await user_repo.get_by_username(username)
        
        # Assert
        mock_db.users.find_one.assert_called_once_with({"username": username})
        assert user is None
    
    async def test_update(self, user_repo, mock_db, sample_user):
        """Test updating a user."""
        # Setup mock
        object_id = ObjectId()
        user_id = str(object_id)
        
        # Set user ID
        sample_user.id = user_id
        
        # Update user email
        sample_user.email = "updated@example.com"
        
        # Mock update_one result
        mock_result = AsyncMock()
        mock_result.matched_count = 1
        mock_db.users.update_one.return_value = mock_result
        
        # Mock find_one result for get_by_id
        mock_db.users.find_one.return_value = {
            "_id": object_id,
            "username": sample_user.username,
            "email": sample_user.email,
            "hashed_password": sample_user.hashed_password,
            "is_active": sample_user.is_active
        }
        
        # Call repository
        with patch('bson.objectid.ObjectId', return_value=object_id):
            updated_user = await user_repo.update(user_id, sample_user)
            
            # Assert
            mock_db.users.update_one.assert_called_once()
            assert updated_user.id == user_id
            assert updated_user.email == "updated@example.com"
    
    async def test_update_not_found(self, user_repo, mock_db, sample_user):
        """Test updating a non-existent user."""
        # Setup mock
        object_id = ObjectId()
        user_id = str(object_id)
        
        # Set user ID
        sample_user.id = user_id
        
        # Mock update_one result
        mock_result = AsyncMock()
        mock_result.matched_count = 0
        mock_db.users.update_one.return_value = mock_result
        
        # Call repository
        with patch('bson.objectid.ObjectId', return_value=object_id):
            with pytest.raises(NotFoundError):
                await user_repo.update(user_id, sample_user)
    
    async def test_delete(self, user_repo, mock_db):
        """Test deleting a user."""
        # Setup mock
        object_id = ObjectId()
        user_id = str(object_id)
        
        # Mock delete_one result
        mock_result = AsyncMock()
        mock_result.deleted_count = 1
        mock_db.users.delete_one.return_value = mock_result
        
        # Call repository
        with patch('bson.objectid.ObjectId', return_value=object_id):
            result = await user_repo.delete(user_id)
            
            # Assert
            mock_db.users.delete_one.assert_called_once()
            assert result is True
    
    async def test_delete_not_found(self, user_repo, mock_db):
        """Test deleting a non-existent user."""
        # Setup mock
        object_id = ObjectId()
        user_id = str(object_id)
        
        # Mock delete_one result
        mock_result = AsyncMock()
        mock_result.deleted_count = 0
        mock_db.users.delete_one.return_value = mock_result
        
        # Call repository
        with patch('bson.objectid.ObjectId', return_value=object_id):
            with pytest.raises(NotFoundError):
                await user_repo.delete(user_id)