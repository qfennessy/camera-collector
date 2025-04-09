# Vintage Camera Collection API Implementation Plan

## Project Initialization and Planning

This document outlines the implementation plan for developing the Vintage Camera Collection API as described in the design document. The implementation will follow a phased approach, using feature branches and test-driven development.

## Progress Tracking

Progress will be tracked using a simple Markdown-based task board in `PROGRESS.md` with the following structure:

```
# Implementation Progress

## Backlog
- Task 1
- Task 2

## In Progress
- Task 3 (Started: YYYY-MM-DD)

## Completed
- Task 4 (Completed: YYYY-MM-DD)
```

Additionally, we'll use GitHub issues to track bugs and feature requests during development.

## Branching Strategy

We'll use the following Git branching strategy:

- `main`: Production-ready code
- `develop`: Integration branch for feature branches
- `feature/*`: Feature branches for new features
- `bugfix/*`: Branches for bug fixes
- `release/*`: Release candidate branches

## Implementation Phases

### Phase 1: Project Setup (1 week)

| Task | Description | Branch | Priority |
|------|-------------|--------|----------|
| Create project structure | Set up basic folder structure according to design doc | `feature/project-structure` | High |
| Set up Poetry | Initialize Poetry and configure pyproject.toml | `feature/poetry-setup` | High |
| Configure pre-commit hooks | Set up pre-commit configuration for code quality | `feature/setup-precommit` | Medium |
| Configure Docker | Create Dockerfile and docker-compose.yml | `feature/docker-setup` | Medium |
| Set up MongoDB connection | Configure database connection and test connectivity | `feature/db-setup` | High |
| Set up pytest | Configure pytest.ini and basic test structure | `feature/test-setup` | High |
| Set up CI/CD | Configure GitHub Actions for CI/CD | `feature/ci-setup` | Medium |

### Phase 2: Core Implementation (2 weeks)

| Task | Description | Branch | Priority |
|------|-------------|--------|----------|
| Implement core models | Create Camera and User models | `feature/core-models` | High |
| Implement database repositories | Create repository layer for MongoDB | `feature/db-repositories` | High |
| Implement services | Create service layer for business logic | `feature/services` | High |
| Implement security | Set up JWT authentication | `feature/auth` | High |
| Implement exception handling | Create custom exceptions and handlers | `feature/exception-handling` | Medium |
| Create API dependencies | Implement dependency injection setup | `feature/api-dependencies` | Medium |

### Phase 3: API Endpoints (2 weeks)

| Task | Description | Branch | Priority |
|------|-------------|--------|----------|
| Implement auth endpoints | Create register, login, refresh endpoints | `feature/auth-endpoints` | High |
| Implement camera CRUD endpoints | Create CRUD endpoints for cameras | `feature/camera-endpoints` | High |
| Implement statistic endpoints | Create statistic endpoints | `feature/stats-endpoints` | Medium |
| Implement image upload | Add image upload functionality | `feature/image-upload` | Medium |
| Configure API docs | Set up Swagger/OpenAPI documentation | `feature/api-docs` | Low |

### Phase 4: Testing (1 week)

| Task | Description | Branch | Priority |
|------|-------------|--------|----------|
| Unit tests | Create unit tests for all components | `feature/unit-tests` | High |
| Integration tests | Create integration tests | `feature/integration-tests` | High |
| API tests | Create API endpoint tests | `feature/api-tests` | High |
| Test coverage | Ensure test coverage meets requirements | `feature/test-coverage` | Medium |

### Phase 5: Optimization and Deployment (1 week)

| Task | Description | Branch | Priority |
|------|-------------|--------|----------|
| Performance optimization | Implement database indexing and caching | `feature/performance` | Medium |
| Security review | Review and enhance security measures | `feature/security-review` | High |
| Documentation | Create README and API documentation | `feature/documentation` | Medium |
| Deployment setup | Create deployment scripts and configurations | `feature/deployment` | High |

## Implementation Checklist for Each Feature

For each feature implementation, follow these steps:

1. Create a new feature branch from `develop`
2. Write tests first (Test-Driven Development)
3. Implement the feature until tests pass
4. Run linters and type checking
5. Create a pull request to merge back to `develop`
6. Code review
7. Merge to `develop` if approved
8. Update progress in `PROGRESS.md`

## Code Quality Standards

- All code must pass linting with ruff
- All code must be formatted with black
- All code must pass mypy type checking
- Minimum test coverage: 80%
- All tests must pass before merging
- Code must be documented with docstrings
- Pre-commit hooks must pass for all commits

## Progress Reporting

Weekly progress reports will be generated with:
- Summary of completed tasks
- Any issues or blockers encountered
- Test coverage report
- Next week's planned tasks

## Initial Setup Commands

Here's a script to initialize the project structure following the modern Python package layout:

```bash
# Initialize Git repository (if not already done)
git init

# Create project structure
mkdir -p camera_collector/{api/{routers,},core,db/repositories,models,services} scripts tests/{api,services,repositories,utils}

# Create __init__.py files
find camera_collector -type d -exec touch {}/__init__.py \;
find tests -type d -exec touch {}/__init__.py \;

# Initialize Poetry
poetry init \
  --name camera_collector \
  --description "A FastAPI application for managing a vintage camera collection" \
  --author "Your Name <your.email@example.com>" \
  --python "^3.9" \
  --dependency fastapi \
  --dependency uvicorn \
  --dependency motor \
  --dependency python-jose \
  --dependency passlib \
  --dependency python-multipart \
  --dependency pydantic \
  --dev-dependency pytest \
  --dev-dependency pytest-asyncio \
  --dev-dependency pytest-cov \
  --dev-dependency httpx \
  --dev-dependency black \
  --dev-dependency ruff \
  --dev-dependency mypy \
  --dev-dependency pre-commit

# Create main application file
cat > camera_collector/main.py << 'EOF'
import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Vintage Camera Collection API",
    description="API for managing a collection of vintage cameras",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Vintage Camera Collection API"}

if __name__ == "__main__":
    uvicorn.run("camera_collector.main:app", host="0.0.0.0", port=8000, reload=True)
EOF

# Create Camera model
cat > camera_collector/models/camera.py << 'EOF'
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
import uuid

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
EOF

# Create pytest configuration
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: Unit tests
    integration: Integration tests
    api: API tests
    slow: Slow tests
addopts = --cov=camera_collector --cov-report=term-missing --cov-fail-under=80
EOF

# Create pre-commit configuration
cat > .pre-commit-config.yaml << 'EOF'
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.262
    hooks:
    -   id: ruff
        args: [--fix]

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
    -   id: mypy
        additional_dependencies: [types-all]
EOF

# Create Docker configuration
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry==1.5.1

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/

# Configure poetry to not use a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy project
COPY . /app/

# Run the application
CMD ["uvicorn", "camera_collector.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Create docker-compose configuration
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mongo
    environment:
      - MONGODB_URL=mongodb://mongo:27017/
      - MONGODB_DB=camera_collector
      - JWT_SECRET=changeme
      - ENVIRONMENT=development

  mongo:
    image: mongo:6.0
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db

volumes:
  mongo-data:
EOF

# Create basic test file
mkdir -p tests/models
cat > tests/models/test_camera.py << 'EOF'
import pytest
from camera_collector.models.camera import Camera

def test_camera_creation():
    camera = Camera(
        brand="Nikon",
        model="F3",
        year_manufactured=1980,
        type="SLR",
        film_format="35mm",
        condition="excellent"
    )
    assert camera.brand == "Nikon"
    assert camera.model == "F3"
    assert camera.year_manufactured == 1980
    assert camera.type == "SLR"
    assert camera.film_format == "35mm"
    assert camera.condition == "excellent"
EOF

# Create version file
echo '__version__ = "0.1.0"' > camera_collector/__init__.py

# Create README
cat > README.md << 'EOF'
# Vintage Camera Collection API

A FastAPI application for managing a collection of vintage cameras.

## Features

- CRUD operations for vintage cameras
- User authentication and authorization
- Statistics on camera collection
- Image upload for cameras

## Getting Started

### Prerequisites

- Python 3.9+
- Poetry
- MongoDB

### Installation

1. Clone the repository
2. Install dependencies with Poetry:
   ```
   poetry install
   ```
3. Run the development server:
   ```
   poetry run python -m camera_collector.main
   ```

## Development

- Run tests: `poetry run pytest`
- Format code: `poetry run black camera_collector tests`
- Lint code: `poetry run ruff check camera_collector tests`
- Type check: `poetry run mypy camera_collector tests`

## Docker

Build and run with Docker Compose:
```
docker-compose up -d
```

## License

[MIT](LICENSE)
EOF

# Create progress tracker
cp PROGRESS_TEMPLATE.md PROGRESS.md

# Install dependencies
poetry install

# Initialize Git repository with initial commit
git add .
git commit -m "Initial project setup"
```

## Test-Driven Development Workflow Example

Here's an example of the TDD workflow for a single feature:

1. Create the test first:

```python
# tests/repositories/test_camera_repository.py
import pytest
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from camera_collector.db.repositories.camera_repository import CameraRepository
from camera_collector.models.camera import Camera

@pytest.mark.asyncio
async def test_create_camera(mongodb):
    # Arrange
    repo = CameraRepository(mongodb)
    camera_data = {
        "brand": "Nikon",
        "model": "F3",
        "year_manufactured": 1980,
        "type": "SLR",
        "film_format": "35mm",
        "condition": "excellent"
    }
    
    # Act
    created_camera = await repo.create(Camera(**camera_data))
    
    # Assert
    assert created_camera.id is not None
    assert created_camera.brand == camera_data["brand"]
    assert created_camera.model == camera_data["model"]
    
    # Cleanup
    await mongodb.cameras.delete_many({})
```

2. Run test (it will fail)
3. Implement the repository:

```python
# camera_collector/db/repositories/camera_repository.py
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from camera_collector.models.camera import Camera

class CameraRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.cameras
    
    async def create(self, camera: Camera) -> Camera:
        """Create a new camera in the database."""
        camera_dict = camera.dict()
        result = await self.collection.insert_one(camera_dict)
        camera.id = str(result.inserted_id)
        return camera
        
    async def get_by_id(self, id: str) -> Optional[Camera]:
        """Get a camera by its ID."""
        camera_dict = await self.collection.find_one({"_id": ObjectId(id)})
        if camera_dict:
            camera_dict["id"] = str(camera_dict.pop("_id"))
            return Camera(**camera_dict)
        return None
        
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Camera]:
        """Get all cameras with pagination."""
        cameras = []
        cursor = self.collection.find().skip(skip).limit(limit)
        async for camera_dict in cursor:
            camera_dict["id"] = str(camera_dict.pop("_id"))
            cameras.append(Camera(**camera_dict))
        return cameras
        
    async def update(self, id: str, camera: Camera) -> Optional[Camera]:
        """Update a camera by its ID."""
        camera_dict = camera.dict(exclude={"id"})
        result = await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": camera_dict}
        )
        if result.modified_count:
            return await self.get_by_id(id)
        return None
        
    async def delete(self, id: str) -> bool:
        """Delete a camera by its ID."""
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
```

4. Create the test fixtures:

```python
# tests/conftest.py
import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def mongodb():
    """Create a MongoDB test database."""
    mongo_url = os.getenv("MONGODB_TEST_URL", "mongodb://localhost:27017")
    mongo_db = os.getenv("MONGODB_TEST_DB", "camera_collector_test")
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[mongo_db]
    
    yield db
    
    # Clean up
    client.drop_database(mongo_db)
    client.close()
```

5. Run the test again (it should pass)
6. Refactor if necessary
7. Update progress tracker

## Regular Review and Adaptation

At the end of each phase:
1. Review completed work
2. Adjust timelines if necessary
3. Update progress tracker
4. Hold retrospective to identify improvements

This approach ensures that progress is visible, tests are written first, and the implementation follows the design while allowing for incremental development and adjustment.