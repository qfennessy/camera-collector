import os
from pydantic import BaseSettings
from typing import Optional, Dict, Any


class Settings(BaseSettings):
    """Application settings.
    
    These settings can be configured using environment variables.
    """
    # Base
    PROJECT_NAME: str = "Vintage Camera API"
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    VERSION: str = "0.1.0"
    
    # MongoDB
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "camera_collector")
    MONGODB_TEST_URL: str = os.getenv("MONGODB_TEST_URL", "mongodb://localhost:27017")
    MONGODB_TEST_DB: str = os.getenv("MONGODB_TEST_DB", "camera_collector_test")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()