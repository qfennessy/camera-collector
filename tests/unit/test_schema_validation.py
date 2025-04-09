import pytest
from pydantic import ValidationError
from datetime import datetime, date

from camera_collector.schemas.camera import CameraCreate, CameraUpdate
from camera_collector.schemas.user import UserCreate, UserUpdate


class TestCameraSchemaValidation:
    """Test camera schema validation."""
    
    def test_camera_create_schema_valid(self):
        """Test creating a valid camera schema."""
        camera_data = {
            "brand": "Nikon",
            "model": "F3",
            "year_manufactured": 1980,
            "type": "SLR",
            "film_format": "35mm",
            "condition": "excellent",
            "special_features": ["high-speed", "titanium shutter"],
            "notes": "Test notes",
            "acquisition_date": "2022-01-15",
            "acquisition_price": 450.00,
            "estimated_value": 500.00
        }
        
        camera = CameraCreate(**camera_data)
        assert camera.brand == "Nikon"
        assert camera.model == "F3"
        assert camera.year_manufactured == 1980
        assert camera.condition == "excellent"
        assert camera.acquisition_price == 450.00
    
    def test_camera_create_schema_invalid_year(self):
        """Test creating a camera with invalid year."""
        # Year too far in the future
        camera_data = {
            "brand": "Nikon",
            "model": "F3",
            "year_manufactured": datetime.now().year + 10,  # 10 years in the future
            "type": "SLR",
            "film_format": "35mm",
            "condition": "excellent"
        }
        
        with pytest.raises(ValidationError) as excinfo:
            CameraCreate(**camera_data)
        
        assert "year_manufactured" in str(excinfo.value)
        
        # Year too far in the past
        camera_data["year_manufactured"] = 1700
        
        with pytest.raises(ValidationError) as excinfo:
            CameraCreate(**camera_data)
        
        assert "year_manufactured" in str(excinfo.value)
    
    def test_camera_create_schema_invalid_condition(self):
        """Test creating a camera with invalid condition."""
        camera_data = {
            "brand": "Nikon",
            "model": "F3",
            "year_manufactured": 1980,
            "type": "SLR",
            "film_format": "35mm",
            "condition": "invalid"  # Invalid condition
        }
        
        with pytest.raises(ValidationError) as excinfo:
            CameraCreate(**camera_data)
        
        assert "condition" in str(excinfo.value)
    
    def test_camera_update_schema_partial(self):
        """Test updating a camera with partial data."""
        update_data = {
            "notes": "Updated notes",
            "condition": "good"
        }
        
        camera_update = CameraUpdate(**update_data)
        assert camera_update.notes == "Updated notes"
        assert camera_update.condition == "good"
        assert camera_update.brand is None
        assert camera_update.model is None
    
    def test_camera_update_schema_invalid(self):
        """Test updating a camera with invalid data."""
        update_data = {
            "condition": "invalid"  # Invalid condition
        }
        
        with pytest.raises(ValidationError) as excinfo:
            CameraUpdate(**update_data)
        
        assert "condition" in str(excinfo.value)


class TestUserSchemaValidation:
    """Test user schema validation."""
    
    def test_user_create_schema_valid(self):
        """Test creating a valid user schema."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        
        user = UserCreate(**user_data)
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "password123"
    
    def test_user_create_schema_invalid_email(self):
        """Test creating a user with invalid email."""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",  # Invalid email
            "password": "password123"
        }
        
        with pytest.raises(ValidationError) as excinfo:
            UserCreate(**user_data)
        
        assert "email" in str(excinfo.value)
    
    def test_user_create_schema_invalid_password(self):
        """Test creating a user with invalid password."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "short"  # Too short
        }
        
        with pytest.raises(ValidationError) as excinfo:
            UserCreate(**user_data)
        
        assert "password" in str(excinfo.value)
    
    def test_user_update_schema_partial(self):
        """Test updating a user with partial data."""
        update_data = {
            "email": "updated@example.com"
        }
        
        user_update = UserUpdate(**update_data)
        assert user_update.email == "updated@example.com"
        assert user_update.username is None
        assert user_update.password is None
    
    def test_user_update_schema_invalid(self):
        """Test updating a user with invalid data."""
        update_data = {
            "email": "invalid-email"  # Invalid email
        }
        
        with pytest.raises(ValidationError) as excinfo:
            UserUpdate(**update_data)
        
        assert "email" in str(excinfo.value)