import pytest
import os
from unittest.mock import patch

from camera_collector.core.config import Settings


class TestConfig:
    """Test configuration settings."""
    
    def test_default_settings(self):
        """Test default settings."""
        settings = Settings()
        
        # Check default values
        assert settings.PROJECT_NAME == "Vintage Camera API"
        assert settings.API_PREFIX == "/api"
        assert settings.DEBUG is False
        assert settings.MONGODB_URL == os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        assert settings.MONGODB_DB == os.getenv("MONGODB_DB", "camera_collector")
        assert settings.ALGORITHM == "HS256"
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 60 * 24  # 1 day
    
    @patch.dict(os.environ, {"PROJECT_NAME": "Test API", "DEBUG": "True"})
    def test_environment_override(self):
        """Test environment variable overrides."""
        settings = Settings()
        
        # Check that environment variables override defaults
        assert settings.PROJECT_NAME == "Test API"
        assert settings.DEBUG is True
    
    @patch.dict(os.environ, {"SECRET_KEY": "test_secret_key"})
    def test_sensitive_settings(self):
        """Test sensitive settings."""
        settings = Settings()
        
        # Check that sensitive settings are properly loaded
        assert settings.SECRET_KEY == "test_secret_key"
    
    def test_cors_settings(self):
        """Test CORS settings."""
        settings = Settings()
        
        # Check CORS settings
        assert settings.CORS_ORIGINS == ["*"]
        assert settings.CORS_METHODS == ["*"]
        assert settings.CORS_HEADERS == ["*"]