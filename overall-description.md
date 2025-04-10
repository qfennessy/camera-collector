# Camera Collector Project

## Overview

The camera-collector project is a FastAPI application designed to manage a collection of vintage cameras. It utilizes MongoDB for data persistence, leveraging its flexibility for storing camera details with varying attributes and metadata.

## Key Features

- **JWT-based Authentication**: Secure user authentication system
- **Comprehensive CRUD Operations**: Complete management of camera collections
- **Advanced Search and Filtering**: Find cameras by various attributes
- **Collection Statistics**: Insights into collection composition and value
- **Image Upload Support**: Store and retrieve camera images

## Architecture

The codebase follows a clean, modular structure with clear separation of concerns:

- **API Layer** (`api/`): FastAPI routes and endpoints
- **Core Components** (`core/`): Configuration, security, and exceptions
- **Data Layer** (`db/`, `models/`, `schemas/`): Database interactions and data models
- **Business Logic** (`services/`): Application services and business rules

## Testing Infrastructure

Integration testing is facilitated via Docker Compose, defined in `docker-compose-test.yml`. This setup includes:

- **Dedicated MongoDB Container**: Isolated `mongodb_test` instance initialized with test data
  - Configured on port 27018 to avoid conflicts with development instances
  - Pre-populated with test users and sample camera data

- **Test Runner Service**: Built using `Dockerfile.test`
  - Executes the pytest suite against the application code
  - Configured with testing-specific environment variables
  - Produces detailed coverage reports

- **Orchestration Script**: `scripts/run_tests.sh` manages:
  - Container lifecycle (build, start, wait for readiness, cleanup)
  - Test execution with appropriate parameters
  - Coverage reporting and result presentation

## Current Status

The project is currently at **Phase 4 (Testing)**, with:

- **Test Coverage**: ~70% (target: 80%)
- **Test Structure**:
  - Unit tests for individual components
  - Integration tests for API endpoints
  - MongoDB integration tests for database operations
  - Specialized authentication tests with bcrypt configuration

Recent improvements include:
- Containerized MongoDB testing environment
- Enhanced bcrypt configuration for authentication testing
- Improved test robustness and reliability

## Next Steps

- Address skipped tests to improve coverage
- Resolve bcrypt compatibility issues in testing
- Complete Phase 5 (Optimization and Deployment)