# Camera Collector API Documentation

## Table of Contents

- [API Overview](#api-overview)
- [Authentication](#authentication)
- [Common Headers](#common-headers)
- [Common Query Parameters](#common-query-parameters)
- [Resources](#resources)
  - [Authentication](#authentication-endpoints)
  - [Cameras](#cameras)
  - [Statistics](#statistics)
- [Error Handling](#error-handling)
- [Middleware](#middleware)

## API Overview

### Base URL Structure

The Camera Collector API is accessible at:

```
http://localhost:8000/api/v1
```

In production environments, the base URL would be:

```
https://api.cameracollector.example.com/api/v1
```

### Authentication Method

The API uses JSON Web Tokens (JWT) for authentication. Tokens must be included in the `Authorization` header as a Bearer token.

### Content Types

The API accepts and returns JSON data:

- Request Content-Type: `application/json`
- Response Content-Type: `application/json`

### Versioning Approach

API versioning is included in the URL path (e.g., `/api/v1/`). This allows for future API versions to be developed without breaking existing clients.

### Health Check Endpoints

```
GET /api/v1/health
```

Response:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2025-04-18T10:00:00.000Z"
}
```

## Authentication

### Authentication Flow

1. Client sends credentials to the login endpoint
2. Server validates credentials and returns a JWT token
3. Client includes the token in subsequent requests via the Authorization header
4. Token includes user information and expiration time
5. Server validates token for protected endpoints

### Token Structure

```python
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenPayload(BaseModel):
    sub: str  # User ID
    exp: datetime
    scopes: list[str] = []
```

## Common Headers

| Header Name | Description | Required | Example |
|-------------|-------------|----------|---------|
| Authorization | Bearer token for authentication | Yes (for protected endpoints) | `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |
| Content-Type | Media type of request body | Yes (for POST/PUT) | `application/json` |
| Accept | Media type(s) accepted by client | No | `application/json` |
| X-Request-ID | Client-generated request identifier | No | `550e8400-e29b-41d4-a716-446655440000` |

## Common Query Parameters

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| page | Page number for paginated results | 1 | `?page=2` |
| page_size | Number of items per page | 10 | `?page_size=20` |
| sort | Field to sort by | None | `?sort=name` |
| sort_dir | Sort direction (asc/desc) | asc | `?sort_dir=desc` |
| q | General search query | None | `?q=leica` |

## Resources

### Authentication Endpoints

#### Login

```
POST /api/v1/auth/login
```

Request Body:
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Register User

```
POST /api/v1/auth/register
```

Request Body:
```json
{
  "email": "user@example.com",
  "username": "johnsmith",
  "password": "password123",
  "full_name": "John Smith"
}
```

Response:
```json
{
  "id": "5f8a3da2a8d2e0a5b9c7f8e2",
  "email": "user@example.com",
  "username": "johnsmith",
  "full_name": "John Smith",
  "created_at": "2025-04-18T10:00:00.000Z"
}
```

### Cameras

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/v1/cameras` | GET | List all cameras | Yes |
| `/api/v1/cameras` | POST | Create a new camera | Yes |
| `/api/v1/cameras/{camera_id}` | GET | Get a specific camera | Yes |
| `/api/v1/cameras/{camera_id}` | PUT | Update a camera | Yes |
| `/api/v1/cameras/{camera_id}` | DELETE | Delete a camera | Yes |
| `/api/v1/cameras/search` | GET | Search cameras | Yes |

#### List Cameras

```
GET /api/v1/cameras
```

Response:
```json
{
  "total": 100,
  "page": 1,
  "page_size": 10,
  "items": [
    {
      "id": "5f8a3da2a8d2e0a5b9c7f8e2",
      "brand": "Leica",
      "model": "M3",
      "year": 1954,
      "type": "rangefinder",
      "format": "35mm",
      "description": "Classic rangefinder camera",
      "condition": "excellent",
      "created_at": "2025-04-18T10:00:00.000Z",
      "updated_at": "2025-04-18T10:00:00.000Z"
    },
    // Additional cameras...
  ]
}
```

#### Create Camera

```
POST /api/v1/cameras
```

Request Body:
```json
{
  "brand": "Nikon",
  "model": "F3",
  "year": 1980,
  "type": "SLR",
  "format": "35mm",
  "description": "Professional 35mm SLR",
  "condition": "good"
}
```

Response:
```json
{
  "id": "5f8a3da2a8d2e0a5b9c7f8e3",
  "brand": "Nikon",
  "model": "F3",
  "year": 1980,
  "type": "SLR",
  "format": "35mm",
  "description": "Professional 35mm SLR",
  "condition": "good",
  "created_at": "2025-04-18T10:00:00.000Z",
  "updated_at": "2025-04-18T10:00:00.000Z"
}
```

#### Get Camera

```
GET /api/v1/cameras/{camera_id}
```

Response:
```json
{
  "id": "5f8a3da2a8d2e0a5b9c7f8e3",
  "brand": "Nikon",
  "model": "F3",
  "year": 1980,
  "type": "SLR",
  "format": "35mm",
  "description": "Professional 35mm SLR",
  "condition": "good",
  "created_at": "2025-04-18T10:00:00.000Z",
  "updated_at": "2025-04-18T10:00:00.000Z"
}
```

#### Update Camera

```
PUT /api/v1/cameras/{camera_id}
```

Request Body:
```json
{
  "brand": "Nikon",
  "model": "F3",
  "year": 1980,
  "type": "SLR",
  "format": "35mm",
  "description": "Professional 35mm SLR with updated metering",
  "condition": "excellent"
}
```

Response:
```json
{
  "id": "5f8a3da2a8d2e0a5b9c7f8e3",
  "brand": "Nikon",
  "model": "F3",
  "year": 1980,
  "type": "SLR",
  "format": "35mm",
  "description": "Professional 35mm SLR with updated metering",
  "condition": "excellent",
  "created_at": "2025-04-18T10:00:00.000Z",
  "updated_at": "2025-04-18T10:00:00.000Z"
}
```

#### Delete Camera

```
DELETE /api/v1/cameras/{camera_id}
```

Response:
```json
{
  "success": true,
  "message": "Camera deleted successfully"
}
```

#### Search Cameras

```
GET /api/v1/cameras/search?q=leica&year=1954
```

Response:
```json
{
  "total": 5,
  "page": 1,
  "page_size": 10,
  "items": [
    {
      "id": "5f8a3da2a8d2e0a5b9c7f8e2",
      "brand": "Leica",
      "model": "M3",
      "year": 1954,
      "type": "rangefinder",
      "format": "35mm",
      "description": "Classic rangefinder camera",
      "condition": "excellent",
      "created_at": "2025-04-18T10:00:00.000Z",
      "updated_at": "2025-04-18T10:00:00.000Z"
    },
    // Additional cameras...
  ]
}
```

### Statistics

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/v1/stats/brands` | GET | Get camera count by brand | Yes |
| `/api/v1/stats/years` | GET | Get camera count by year | Yes |
| `/api/v1/stats/formats` | GET | Get camera count by format | Yes |

#### Get Camera Count by Brand

```
GET /api/v1/stats/brands
```

Response:
```json
{
  "brands": [
    {"name": "Leica", "count": 15},
    {"name": "Nikon", "count": 12},
    {"name": "Canon", "count": 10},
    {"name": "Pentax", "count": 8},
    {"name": "Olympus", "count": 5}
  ]
}
```

#### Get Camera Count by Year

```
GET /api/v1/stats/years
```

Response:
```json
{
  "years": [
    {"year": 1950, "count": 5},
    {"year": 1960, "count": 12},
    {"year": 1970, "count": 18},
    {"year": 1980, "count": 15},
    {"year": 1990, "count": 8}
  ]
}
```

#### Get Camera Count by Format

```
GET /api/v1/stats/formats
```

Response:
```json
{
  "formats": [
    {"format": "35mm", "count": 25},
    {"format": "medium format", "count": 10},
    {"format": "large format", "count": 5},
    {"format": "APS-C", "count": 8},
    {"format": "half frame", "count": 2}
  ]
}
```

## Error Handling

### Standardized Error Format

All API errors are returned in a consistent format:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Camera with ID '5f8a3da2a8d2e0a5b9c7f8e9' not found",
    "details": {
      "camera_id": "5f8a3da2a8d2e0a5b9c7f8e9"
    }
  }
}
```

### Common Error Types

| Error Code | Description |
|------------|-------------|
| VALIDATION_ERROR | Request validation failed |
| NOT_FOUND | Requested resource not found |
| UNAUTHORIZED | Authentication required |
| FORBIDDEN | User lacks required permissions |
| INTERNAL_ERROR | Server error occurred |
| CONFLICT | Resource conflict (e.g., duplicate entry) |

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request format or parameters |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource conflict |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

## Middleware

The API uses several middleware components to process requests:

1. **Authentication Middleware**: Validates JWT tokens and adds user information to request context
2. **CORS Middleware**: Handles Cross-Origin Resource Sharing
3. **Logging Middleware**: Logs request and response information
4. **Error Handling Middleware**: Catches exceptions and returns standardized error responses
5. **Request ID Middleware**: Generates or propagates request IDs for tracing