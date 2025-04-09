# Vintage Camera Collection API

A FastAPI application for managing a collection of vintage cameras. This API provides a comprehensive way to track, manage, and search for vintage cameras in your collection.

## Features

- User authentication with JWT tokens
- CRUD operations for camera collection
- Advanced search and filtering
- Statistics about your collection
- Image upload support
- MongoDB database for flexible storage

## Getting Started

### Prerequisites

- Python 3.9+
- Poetry (dependency management)
- MongoDB
- Docker (optional, for containerized development)

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/camera-collector.git
   cd camera-collector
   ```

2. Install dependencies with Poetry
   ```
   poetry install
   ```

3. Configure environment variables
   ```
   export MONGODB_URL="mongodb://localhost:27017"
   export MONGODB_DB="camera_collector"
   export SECRET_KEY="your-secret-key"
   ```

4. Run the development server
   ```
   poetry run uvicorn camera_collector.main:app --reload
   ```

5. The API will be available at http://localhost:8000

### Using Docker

1. Start the application and MongoDB with Docker Compose
   ```
   docker-compose up -d
   ```

2. The API will be available at http://localhost:8000

## Running Tests

### Running Tests Locally

```
poetry run pytest
```

### Running Tests with Mock Database

```
poetry run pytest --cov=camera_collector
```

### Running Tests with MongoDB Container

We provide a Docker-based testing environment that includes a MongoDB container:

```
./scripts/run_tests.sh
```

This script:
1. Starts a MongoDB container for testing
2. Runs the tests
3. Generates a coverage report
4. Cleans up the containers

The coverage report is available at `./reports/coverage/index.html`

## Project Structure

```
camera_collector/
├── api/               # API routes and dependencies
├── core/              # Core application components
├── db/                # Database models and repositories
├── models/            # Domain models
├── schemas/           # Pydantic schemas for validation
├── services/          # Business logic services
└── main.py            # Application entry point

tests/
├── api/               # API endpoint tests
├── integration/       # Integration tests
├── models/            # Model tests
├── repositories/      # Repository tests
├── services/          # Service tests
└── unit/              # Unit tests for core components
```

## API Documentation

When the server is running, documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

This project is licensed under the MIT License - see the LICENSE file for details.
