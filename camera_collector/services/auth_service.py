from datetime import timedelta
from typing import Optional, Tuple

from camera_collector.core.config import settings
from camera_collector.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token
)
from camera_collector.db.repositories.user_repository import UserRepository
from camera_collector.models.user import User
from camera_collector.schemas.user import UserCreate, UserResponse
from camera_collector.schemas.auth import TokenResponse
from camera_collector.core.exceptions import AuthenticationError, ValidationError


class AuthService:
    """Authentication and authorization service."""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def register_user(self, user_data: UserCreate) -> UserResponse:
        """Register a new user.
        
        Args:
            user_data: User registration data
            
        Returns:
            Created user
            
        Raises:
            ValidationError: If username or email already exists
        """
        # Check if username already exists
        existing_user = await self.user_repository.get_by_username(user_data.username)
        if existing_user:
            raise ValidationError("Username already registered")
        
        # Check if email already exists
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValidationError("Email already registered")
        
        # Create user with hashed password
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=get_password_hash(user_data.password),
            is_active=True
        )
        
        created_user = await self.user_repository.create(user)
        return UserResponse.from_orm(created_user)
    
    async def authenticate_user(self, username: str, password: str) -> User:
        """Authenticate a user with username and password.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Authenticated user
            
        Raises:
            AuthenticationError: If authentication fails
        """
        user = await self.user_repository.get_by_username(username)
        if not user:
            raise AuthenticationError("Invalid username or password")
        
        if not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid username or password")
        
        if not user.is_active:
            raise AuthenticationError("User account is inactive")
        
        return user
    
    async def login(self, username: str, password: str) -> TokenResponse:
        """Login a user and generate access and refresh tokens.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Token response with access and refresh tokens
            
        Raises:
            AuthenticationError: If authentication fails
        """
        user = await self.authenticate_user(username, password)
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        
        access_token = create_access_token(user.id, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(user.id, expires_delta=refresh_token_expires)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Generate new access and refresh tokens from a refresh token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            New token response
            
        Raises:
            AuthenticationError: If token is invalid
        """
        from jose import jwt, JWTError
        
        try:
            # Decode refresh token
            payload = jwt.decode(
                refresh_token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")
            
            if user_id is None:
                raise AuthenticationError("Invalid refresh token")
            
            # Get user from database
            user = await self.user_repository.get_by_id(user_id)
            
            # Generate new tokens
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
            
            access_token = create_access_token(user.id, expires_delta=access_token_expires)
            new_refresh_token = create_refresh_token(user.id, expires_delta=refresh_token_expires)
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=new_refresh_token
            )
        
        except JWTError:
            raise AuthenticationError("Invalid refresh token")