# Vintage Camera Collection API Design

## Overview
This document outlines the design for a FastAPI-based RESTful API that provides CRUD operations for managing a collection of vintage cameras using a NoSQL database.

## Technology Stack
- **Framework**: FastAPI
- **Database**: MongoDB (NoSQL)
- **Authentication**: JWT-based authentication
- **Documentation**: Automatic via Swagger/OpenAPI
- **Validation**: Pydantic models
- **Testing**: pytest, pytest-asyncio, pytest-cov
- **Package Management**: Poetry

## Data Model

### Camera
```python
class Camera(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    brand: str
    model: str
    year_manufactured: int
    type: str  # e.g., SLR, TLR, rangefinder, etc.
    film_format: str  # e.g., 35mm, 120, 4x5, etc.
    condition: str  # e.g., mint, excellent, good, fair, poor
    special_features: List[str] = []
    notes: Optional[str] = None
    acquisition_date: Optional[date] = None
    acquisition_price: Optional[float] = None
    estimated_value: Optional[float] = None
    images: List[str] = []  # URLs to camera images
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/refresh` - Refresh JWT token

### Cameras
- `GET /api/cameras` - List all cameras (with pagination, filtering, sorting)
- `POST /api/cameras` - Create a new camera
- `GET /api/cameras/{camera_id}` - Get camera details
- `PUT /api/cameras/{camera_id}` - Update camera details
- `DELETE /api/cameras/{camera_id}` - Delete camera
- `POST /api/cameras/{camera_id}/images` - Upload camera images

### Statistics
- `GET /api/stats/brands` - Get camera count by brand
- `GET /api/stats/types` - Get camera count by type
- `GET /api/stats/decades` - Get camera count by decade of manufacture
- `GET /api/stats/value` - Get total collection value

## Project Structure
```
camera_collector/
├── pyproject.toml            # Poetry package definition and dependencies
├── README.md                 # Project documentation
├── .gitignore
├── .pre-commit-config.yaml   # Pre-commit hooks
├── pytest.ini                # Pytest configuration
├── Dockerfile
├── docker-compose.yml
├── camera_collector/         # Main package source
│   ├── __init__.py           # Package version and metadata
│   ├── main.py               # FastAPI application entry point
│   ├── api/                  # API layer
│   │   ├── __init__.py
│   │   ├── dependencies.py   # FastAPI dependencies
│   │   ├── routers/          # API route definitions
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── cameras.py
│   │   │   └── stats.py
│   ├── core/                 # Core application code
│   │   ├── __init__.py
│   │   ├── config.py         # Application configuration
│   │   ├── security.py       # Authentication and security
│   │   └── exceptions.py     # Custom exceptions
│   ├── db/                   # Database layer
│   │   ├── __init__.py
│   │   ├── database.py       # Database connection
│   │   └── repositories/     # Data access objects
│   │       ├── __init__.py
│   │       └── camera_repository.py
│   ├── models/               # Pydantic models (schema definitions)
│   │   ├── __init__.py
│   │   ├── camera.py
│   │   └── user.py
│   └── services/             # Business logic
│       ├── __init__.py
│       ├── auth_service.py
│       └── camera_service.py
├── scripts/                  # Utility scripts
│   ├── seed_data.py          # Script to populate test data
│   └── setup_db.py           # Database setup script
└── tests/                    # Test suite
    ├── __init__.py
    ├── conftest.py           # Test fixtures and configuration
    ├── api/                  # API tests
    │   ├── __init__.py
    │   ├── test_auth.py
    │   ├── test_cameras.py
    │   └── test_stats.py
    ├── services/             # Service layer tests
    │   ├── __init__.py
    │   ├── test_auth_service.py
    │   └── test_camera_service.py
    ├── repositories/         # Repository tests
    │   ├── __init__.py
    │   └── test_camera_repository.py
    └── utils/                # Test utilities
        ├── __init__.py
        ├── test_fixtures.py
        └── test_helpers.py
```

## Security Considerations
- JWT-based authentication
- Data validation using Pydantic
- Rate limiting for API endpoints
- Input sanitization
- CORS configuration

## Performance Optimizations
- Database indexing (brand, type, year_manufactured)
- Pagination for list endpoints
- Query optimization
- Caching frequently accessed data

## Testing Strategy

### Test Types
- **Unit Tests**: Testing individual components in isolation
- **Integration Tests**: Testing interaction between components
- **API Tests**: Testing the API endpoints
- **Performance Tests**: Testing the API performance under load

### Test Structure

#### Unit Tests
- Test individual services, repositories, and utility functions
- Mock external dependencies (database, auth, etc.)
- Focus on business logic and edge cases

#### Integration Tests
- Test interaction between components (e.g., service + repository)
- Use test database for database integration tests
- Test complete workflows end-to-end

#### API Tests
- Test all API endpoints
- Test authentication and authorization
- Test input validation and error handling
- Test response formats and status codes

### Test Fixtures and Mocks
- MongoDB test database setup and teardown
- Test data generation
- Authentication token generation for protected endpoints
- Mocking external services

### Test Configuration

```python
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: Unit tests (fast tests that don't require external dependencies)
    integration: Integration tests (tests that require external dependencies)
    api: API tests (tests that test the API endpoints)
    slow: Slow tests that take more than 1 second to run
addopts = --cov=camera_collector --cov-report=term-missing --cov-fail-under=80
```

### Example Test Cases

#### Repository Tests
```python
# tests/repositories/test_camera_repository.py
import pytest
from bson import ObjectId
from camera_collector.db.repositories.camera_repository import CameraRepository

@pytest.mark.integration
async def test_create_camera(test_db, camera_data):
    repo = CameraRepository(test_db)
    camera = await repo.create(camera_data)
    assert camera.id is not None
    assert camera.brand == camera_data["brand"]
    assert camera.model == camera_data["model"]
    
@pytest.mark.integration
async def test_get_camera_by_id(test_db, test_camera):
    repo = CameraRepository(test_db)
    camera = await repo.get_by_id(test_camera.id)
    assert camera is not None
    assert camera.id == test_camera.id
```

#### Service Tests
```python
# tests/services/test_camera_service.py
import pytest
from unittest.mock import AsyncMock, patch
from camera_collector.services.camera_service import CameraService

@pytest.mark.unit
async def test_create_camera_service():
    mock_repo = AsyncMock()
    mock_repo.create.return_value = {"id": "123", "brand": "Nikon", "model": "F3"}
    
    service = CameraService(mock_repo)
    result = await service.create_camera({"brand": "Nikon", "model": "F3"})
    
    mock_repo.create.assert_called_once()
    assert result["brand"] == "Nikon"
```

#### API Tests
```python
# tests/api/test_cameras.py
import pytest
from fastapi.testclient import TestClient
from camera_collector.main import app

@pytest.mark.api
def test_create_camera(test_client, auth_headers, camera_data):
    response = test_client.post("/api/cameras", json=camera_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["brand"] == camera_data["brand"]
    assert data["model"] == camera_data["model"]

@pytest.mark.api
def test_get_camera_list(test_client, auth_headers):
    response = test_client.get("/api/cameras", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
```

### Test Fixtures
```python
# tests/conftest.py
import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from camera_collector.core.config import settings
from camera_collector.models.camera import Camera

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_db():
    client = AsyncIOMotorClient(settings.MONGODB_TEST_URI)
    db = client[settings.MONGODB_TEST_DB]
    yield db
    client.drop_database(settings.MONGODB_TEST_DB)
    client.close()

@pytest.fixture
def test_client():
    from camera_collector.main import app
    with TestClient(app) as client:
        yield client

@pytest.fixture
def auth_headers(test_client):
    response = test_client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
async def test_camera(test_db):
    camera_data = {
        "brand": "Leica",
        "model": "M3",
        "year_manufactured": 1954,
        "type": "rangefinder",
        "film_format": "35mm",
        "condition": "excellent"
    }
    result = await test_db.cameras.insert_one(camera_data)
    camera_data["id"] = str(result.inserted_id)
    yield Camera(**camera_data)
    await test_db.cameras.delete_one({"_id": result.inserted_id})
```

## CI/CD Pipeline
- GitHub Actions for CI/CD
- Run tests on each pull request
- Generate code coverage reports
- Build and push Docker image on successful merge to main

## Future Enhancements
- Image processing and thumbnail generation
- Export/import functionality (CSV, JSON)
- Advanced search capabilities
- User roles and permissions
- Activity logging
- Camera maintenance records
- Integration with camera valuation APIs