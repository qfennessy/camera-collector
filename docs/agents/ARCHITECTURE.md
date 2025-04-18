# Camera Collector System Architecture

## Table of Contents

- [System Overview](#system-overview)
- [System Interaction Diagram](#system-interaction-diagram)
- [Technology Stack](#technology-stack)
- [Major Components](#major-components)
  - [Backend](#backend)
  - [API Layer](#api-layer)
  - [Database Layer](#database-layer)
  - [Service Layer](#service-layer)
- [Cross-cutting Concerns](#cross-cutting-concerns)
- [Future Architecture Considerations](#future-architecture-considerations)
- [Debugging and Development Guidelines](#debugging-and-development-guidelines)
- [Utility Components](#utility-components)
- [Appendix](#appendix)
  - [Glossary](#glossary)
  - [Common Development Tasks](#common-development-tasks)
  - [Environment Compatibility](#environment-compatibility)
  - [Contribution Guidelines](#contribution-guidelines)

## System Overview

The Camera Collector system is a web-based application designed to catalog and manage vintage camera collections. The system consists of several major components working together to provide a comprehensive solution for camera enthusiasts to document, search, and share their collections.

The system follows a layered architecture pattern with clear separation of concerns:

1. **API Layer**: Handles HTTP requests and responses using FastAPI
2. **Service Layer**: Contains business logic and orchestrates operations
3. **Repository Layer**: Abstracts database operations
4. **Database Layer**: Manages data persistence using MongoDB
5. **Models**: Defines data structures and validation using Pydantic

## System Interaction Diagram

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │──────▶    API      │──────▶   Service   │──────▶ Repository  │
│  (Browser)  │◀─────┤   Layer     │◀─────┤    Layer    │◀─────┤   Layer     │
└─────────────┘      └─────────────┘      └─────────────┘      └─────────────┘
                                                                      │
                                                                      ▼
                                                               ┌─────────────┐
                                                               │  Database   │
                                                               │  (MongoDB)  │
                                                               └─────────────┘
```

## Technology Stack

| Component         | Technology                                 | Purpose                               |
|-------------------|-------------------------------------------|---------------------------------------|
| API Framework     | FastAPI                                   | Web API framework                     |
| Data Validation   | Pydantic                                  | Schema validation and serialization   |
| Database          | MongoDB                                   | Data persistence                      |
| Authentication    | JWT, bcrypt                               | User authentication and security      |
| Testing           | pytest                                    | Unit and integration testing          |
| Documentation     | FastAPI Swagger/ReDoc                     | API documentation                     |
| Containerization  | Docker, Docker Compose                    | Application packaging and deployment  |
| Dependency Management | Poetry                                | Python package management             |
| Code Quality      | black, ruff, mypy                         | Formatting, linting, type checking    |

## Major Components

### Backend

#### Key Architectural Layers

1. **API Layer** (`camera_collector/api/`)
   - Responsible for handling HTTP requests/responses
   - Defines API routes and endpoints
   - Handles request validation
   - Manages dependencies and authentication

2. **Service Layer** (`camera_collector/services/`)
   - Implements business logic
   - Orchestrates operations across repositories
   - Handles error conditions and exceptions

3. **Repository Layer** (`camera_collector/db/repositories/`)
   - Abstracts database operations
   - Provides interface for data access
   - Implements CRUD operations for entities

4. **Models** (`camera_collector/models/`)
   - Defines core data structures
   - Represents database entities

5. **Schemas** (`camera_collector/schemas/`)
   - Defines data validation and serialization
   - Represents API request/response models

#### Directory Structure

```
camera_collector/
├── __init__.py
├── api/
│   ├── __init__.py
│   ├── dependencies.py      # Dependency injection setup
│   └── routers/            # API route definitions
│       ├── __init__.py
│       ├── auth.py         # Authentication endpoints
│       ├── cameras.py      # Camera management endpoints
│       └── stats.py        # Statistics endpoints
├── core/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── exceptions.py       # Custom exception classes
│   └── security.py         # Security utilities
├── db/
│   ├── __init__.py
│   ├── database.py         # Database connection management
│   └── repositories/       # Repository pattern implementations
│       ├── __init__.py
│       ├── camera_repository.py
│       └── user_repository.py
├── main.py                 # Application entry point
├── models/                 # Core domain models
│   ├── __init__.py
│   ├── camera.py
│   ├── token.py
│   └── user.py
├── schemas/               # Pydantic schemas for validation
│   ├── auth.py
│   ├── camera.py
│   └── user.py
└── services/              # Business logic services
    ├── __init__.py
    ├── auth_service.py
    └── camera_service.py
```

#### Key Architectural Patterns

1. **Repository Pattern**
   
   The repository pattern isolates the data layer from the rest of the application:

   ```python
   class CameraRepository:
       def __init__(self, db: Database):
           self.db = db
           self.collection = db.cameras

       async def find_by_id(self, camera_id: str) -> Optional[CameraModel]:
           camera_data = await self.collection.find_one({"_id": ObjectId(camera_id)})
           if camera_data:
               return CameraModel(**camera_data)
           return None
   ```

2. **Dependency Injection**
   
   FastAPI's dependency injection system is used to provide dependencies:

   ```python
   @router.get("/{camera_id}", response_model=CameraResponse)
   async def get_camera(
       camera_id: str, 
       camera_service: CameraService = Depends(get_camera_service)
   ):
       return await camera_service.get_camera(camera_id)
   ```

3. **Service Layer Pattern**
   
   Business logic is encapsulated in service classes:

   ```python
   class CameraService:
       def __init__(self, repository: CameraRepository):
           self.repository = repository

       async def get_camera(self, camera_id: str) -> CameraModel:
           camera = await self.repository.find_by_id(camera_id)
           if not camera:
               raise CameraNotFoundException(camera_id)
           return camera
   ```

#### Authentication Flow

Authentication is implemented using JWT (JSON Web Tokens):

1. User login credentials are validated
2. JWT token is generated with user claims
3. Token is returned to client
4. Client includes token in Authorization header
5. API endpoints validate token and extract user information
6. Authorization rules are applied based on user claims

#### Configuration Management

Configuration is managed through environment variables and a centralized config module:

```python
class Settings(BaseSettings):
    APP_NAME: str = "Camera Collector API"
    DEBUG: bool = False
    MONGODB_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

#### Logging Architecture

The application uses Python's built-in logging module, configured in the main application startup:

```python
def configure_logging():
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
```

#### Performance and Scalability Considerations

1. **Asynchronous I/O**: FastAPI and async MongoDB driver for non-blocking I/O
2. **Connection Pooling**: Database connection pooling to limit resource usage
3. **Pagination**: API endpoints support pagination for large collections
4. **Indexing**: MongoDB indexes for optimized queries
5. **Caching**: Prepared for future implementation of response caching

## Cross-cutting Concerns

1. **Error Handling**: Centralized exception handling with custom exception classes
2. **Authentication**: JWT-based authentication across API endpoints
3. **Validation**: Pydantic models for consistent data validation
4. **Logging**: Structured logging throughout the application
5. **Configuration**: Environment-based configuration management

## Future Architecture Considerations

1. **Caching Layer**: Implement Redis for caching frequently accessed data
2. **Microservices**: Potential split into specialized microservices for specific domains
3. **Event-driven Architecture**: Implement message queue for handling asynchronous tasks
4. **Full-text Search**: Integrate with Elasticsearch for advanced search capabilities
5. **CDN Integration**: Support for image CDN to serve camera images

## Debugging and Development Guidelines

1. **Local Development**:
   - Use Poetry for dependency management
   - Run FastAPI with hot reload for development
   - Set environment variables through `.env` file

2. **Testing**:
   - Write tests for all new features and bug fixes
   - Use pytest fixtures for common test setup
   - Aim for at least 80% test coverage

3. **Debugging**:
   - Use FastAPI's debug mode to see detailed error traces
   - Leverage structured logging for runtime information
   - Set up MongoDB connection monitoring

## Utility Components

1. **Security Utilities**: JWT token handling, password hashing
2. **Exception Classes**: Custom exceptions with HTTP status codes
3. **Database Utilities**: Connection management, transaction handling
4. **API Dependencies**: Reusable dependency functions for endpoints

## Appendix

### Glossary

| Term | Definition |
|------|------------|
| Repository | Pattern that abstracts data access logic |
| DTO | Data Transfer Object - structures used to pass data between application layers |
| JWT | JSON Web Token - method for securely transmitting information as a JSON object |
| Pydantic | Library for data validation and settings management using Python type annotations |
| FastAPI | Modern, fast web framework for building APIs with Python |
| MongoDB | NoSQL document database |
| CRUD | Create, Read, Update, Delete - basic operations for persistence |

### Common Development Tasks

| Task | Command |
|------|---------|
| Setup environment | `poetry install --with dev` |
| Run server | `poetry run python -m camera_collector.main` |
| Format code | `poetry run black camera_collector tests` |
| Run linter | `poetry run ruff check camera_collector tests` |
| Run type checker | `poetry run mypy camera_collector tests` |
| Run tests | `poetry run pytest` |
| Run tests with coverage | `poetry run pytest --cov=camera_collector --cov-report=term-missing` |

### Environment Compatibility

| Component | Development | Testing | Production |
|-----------|------------|---------|------------|
| API Server | ✅ | ✅ | ✅ |
| MongoDB | ✅ | ✅ | ✅ |
| Docker | ✅ | ✅ | ✅ |
| Local Auth | ✅ | ✅ | ✅ |

### Contribution Guidelines

1. **Branch Naming**:
   - Use `feature/*` for new features
   - Use `bugfix/*` for bug fixes
   - Use `release/*` for release preparations

2. **Code Style**:
   - Follow PEP 8 style guidelines
   - Use Black for code formatting
   - Add type annotations to all functions
   - Write docstrings for public methods

3. **Testing**:
   - Write unit tests for all new functionality
   - Ensure existing tests pass before submitting changes
   - Maintain code coverage of at least 80%

4. **Pull Requests**:
   - Reference related issues in PR description
   - Ensure all CI checks pass
   - Keep PRs focused on a single concern
   - Request code reviews from team members