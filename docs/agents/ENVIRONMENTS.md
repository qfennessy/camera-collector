# Camera Collector Environments Guide

## Table of Contents

- [Environment Overview](#environment-overview)
- [Development Environment](#development-environment)
- [Testing Environment](#testing-environment)
- [Production Environment](#production-environment)
- [Environment Compatibility Matrix](#environment-compatibility-matrix)
- [Working with Multiple Environments](#working-with-multiple-environments)
- [Configuration Files](#configuration-files)

## Environment Overview

The Camera Collector system supports multiple deployment environments to facilitate development, testing, and production usage. Each environment has specific configurations and purposes.

| Environment | Description | Hosting | Access Control |
|-------------|-------------|---------|---------------|
| Development | Local environment for active development | Local machine | Developer only |
| Testing | Environment for automated tests | Docker containers or CI/CD pipeline | CI/CD system, Developers |
| Production | Live environment for end users | Cloud hosting | Restricted access, End users |

## Development Environment

### Configuration

The development environment is designed for local development work and debugging.

| Setting | Value | Description |
|---------|-------|-------------|
| Debug Mode | Enabled | Shows detailed error information |
| Database | MongoDB (local or containerized) | Data persistence |
| Authentication | JWT tokens with longer expiry | User authentication |
| Logging | Verbose (DEBUG level) | Detailed logging for debugging |

### Usage Guidelines

- Use for active development and local testing
- Not suitable for performance testing
- Can use dummy data and mock services
- Database can be reset as needed

### Access Control

- Accessible only on local machine
- No special authentication for services
- Default test accounts available

### Environment Variables

```
# Development Environment Variables
DEBUG=True
APP_NAME="Camera Collector API (Development)"
MONGODB_URL="mongodb://localhost:27017/camera_collector_dev"
SECRET_KEY="dev_secret_key_change_in_production"
ACCESS_TOKEN_EXPIRE_MINUTES=60
LOG_LEVEL="DEBUG"
```

## Testing Environment

### Configuration

The testing environment is isolated and configured specifically for running automated tests.

| Setting | Value | Description |
|---------|-------|-------------|
| Debug Mode | Disabled | Production-like error handling |
| Database | MongoDB (containerized) | Isolated test database |
| Authentication | JWT tokens | Standard auth flow |
| Logging | Minimal (ERROR level) | Focused on errors only |

### Usage Guidelines

- Used for running automated tests
- Database is reset before each test run
- Contains seed data for consistent test results
- Simulates production but with isolated resources

### Access Control

- Accessible within Docker network or CI/CD pipeline
- Test credentials only

### Environment Variables

```
# Testing Environment Variables
DEBUG=False
APP_NAME="Camera Collector API (Testing)"
MONGODB_URL="mongodb://mongo:27017/camera_collector_test"
SECRET_KEY="test_secret_key"
ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL="ERROR"
TESTING=True
```

## Production Environment

### Configuration

The production environment is optimized for performance, security, and reliability.

| Setting | Value | Description |
|---------|-------|-------------|
| Debug Mode | Disabled | No sensitive information in errors |
| Database | MongoDB (managed service) | Production database with backups |
| Authentication | JWT tokens with standard expiry | Secure authentication |
| Logging | Standard (INFO level) | Balance of information and performance |

### Usage Guidelines

- Used for live application serving real users
- Data must be backed up regularly
- Performance monitoring enabled
- Security measures fully implemented

### Access Control

- Restricted access to server and infrastructure
- Production credentials securely stored
- HTTPS required for all connections

### Environment Variables

```
# Production Environment Variables
DEBUG=False
APP_NAME="Camera Collector API"
MONGODB_URL="mongodb+srv://user:password@cluster.mongodb.net/camera_collector_prod"
SECRET_KEY="secure_random_generated_key"
ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL="INFO"
CORS_ORIGINS="https://cameracollector.example.com"
```

## Environment Compatibility Matrix

This matrix shows which components and features are available in each environment.

| Component/Feature | Development | Testing | Production |
|-------------------|-------------|---------|------------|
| API Server | ✅ | ✅ | ✅ |
| MongoDB | ✅ (local) | ✅ (container) | ✅ (managed) |
| JWT Authentication | ✅ | ✅ | ✅ |
| Detailed Logging | ✅ | ❌ | ❌ |
| HTTPS | ❌ | ❌ | ✅ |
| Rate Limiting | ❌ | ✅ | ✅ |
| Test Accounts | ✅ | ✅ | ❌ |
| Performance Monitoring | ❌ | ❌ | ✅ |
| Automated Backups | ❌ | ❌ | ✅ |
| OpenAPI Documentation | ✅ | ✅ | ✅ |
| Hot Reload | ✅ | ❌ | ❌ |

## Working with Multiple Environments

### Environment Variable Configuration

The Camera Collector system primarily uses environment variables for configuration across different environments. These can be set in various ways:

1. **Direct environment variables**: Set in the shell before running the application
2. **`.env` files**: Environment-specific configuration files
3. **Docker environment files**: For containerized deployments
4. **CI/CD pipeline variables**: For testing and deployment

### Profile System

The application uses a simple profile system to load environment-specific settings:

1. Create environment-specific `.env` files:
   - `.env.development`
   - `.env.testing`
   - `.env.production`

2. Set the `APP_ENV` environment variable to select the profile:
   ```bash
   export APP_ENV=development
   ```

3. The application will load the appropriate `.env` file based on the `APP_ENV` value.

### Switching Between Environments

For development work, you can easily switch between environments:

```bash
# Switch to development environment
export APP_ENV=development
poetry run python -m camera_collector.main

# Switch to testing environment
export APP_ENV=testing
poetry run python -m camera_collector.main

# Run tests in testing environment
poetry run pytest
```

Docker environments can be selected using docker-compose files:

```bash
# Run development environment
docker-compose up

# Run testing environment
docker-compose -f docker-compose-test.yml up
```

## Configuration Files

| File | Location | Purpose |
|------|----------|---------|
| `.env.example` | Project root | Template for environment variables |
| `.env` | Project root | Local development environment variables |
| `.env.testing` | Project root | Testing environment variables |
| `pyproject.toml` | Project root | Python package configuration |
| `pytest.ini` | Project root | Test runner configuration |
| `docker-compose.yml` | Project root | Development environment containers |
| `docker-compose-test.yml` | Project root | Testing environment containers |
| `Dockerfile` | Project root | Production container configuration |
| `Dockerfile.test` | Project root | Testing container configuration |
| `camera_collector/core/config.py` | Source code | Configuration management module |
| `scripts/mongo-init-test.js` | Scripts directory | MongoDB test instance initialization |

### Sample Configuration Files

#### .env.example
```
# Application
APP_NAME=Camera Collector API
DEBUG=False

# MongoDB
MONGODB_URL=mongodb://localhost:27017/camera_collector

# Security
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongo:27017/camera_collector
      - DEBUG=True
      - SECRET_KEY=dev_secret_key
    volumes:
      - ./:/app
    depends_on:
      - mongo
    command: uvicorn camera_collector.main:app --host 0.0.0.0 --port 8000 --reload

  mongo:
    image: mongo:4.4
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

#### docker-compose-test.yml
```yaml
version: '3.8'

services:
  api_test:
    build:
      context: .
      dockerfile: Dockerfile.test
    environment:
      - MONGODB_URL=mongodb://mongo_test:27017/camera_collector_test
      - DEBUG=False
      - SECRET_KEY=test_secret_key
      - TESTING=True
    depends_on:
      - mongo_test
    command: pytest

  mongo_test:
    image: mongo:4.4
    volumes:
      - ./scripts/mongo-init-test.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
```