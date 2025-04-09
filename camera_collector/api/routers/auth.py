from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from camera_collector.services.auth_service import AuthService
from camera_collector.api.dependencies import get_auth_service
from camera_collector.schemas.auth import TokenResponse, RefreshRequest
from camera_collector.schemas.user import UserCreate, UserResponse
from camera_collector.core.exceptions import ValidationError, AuthenticationError


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
    },
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Register a new user.
    
    Args:
        user_data: User registration data
        auth_service: Auth service dependency
    
    Returns:
        Created user
    
    Raises:
        ValidationError: If validation fails
    """
    try:
        return await auth_service.register_user(user_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    """Login user and return access token.
    
    Args:
        form_data: Login form data
        auth_service: Auth service dependency
    
    Returns:
        Access and refresh tokens
    
    Raises:
        AuthenticationError: If authentication fails
    """
    try:
        return await auth_service.login(form_data.username, form_data.password)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Refresh access token using refresh token.
    
    Args:
        refresh_data: Refresh token data
        auth_service: Auth service dependency
    
    Returns:
        New access and refresh tokens
    
    Raises:
        AuthenticationError: If token is invalid
    """
    try:
        return await auth_service.refresh_token(refresh_data.refresh_token)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )