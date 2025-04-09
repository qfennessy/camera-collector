from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    """Raised when a resource is not found."""
    
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AuthenticationError(HTTPException):
    """Raised when authentication fails."""
    
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(HTTPException):
    """Raised when user doesn't have permission to access a resource."""
    
    def __init__(self, detail: str = "Not authorized to perform this action"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ValidationError(HTTPException):
    """Raised when data validation fails."""
    
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class DatabaseError(HTTPException):
    """Raised when a database operation fails."""
    
    def __init__(self, detail: str = "Database error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)