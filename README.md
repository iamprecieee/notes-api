# Overview

Multi-tenant Notes API with role-based access control. Built with FastAPI and MongoDB.

## Features

- Multi-tenant architecture with organization isolation
- Role-based access control (reader, writer, admin)
- JWT authentication with middleware
- Email unique per organization
- Organization names are globally unique
- MongoDB with Beanie ODM
- Automatic admin assignment for first user in each organization

## Architecture

Three-layer architecture:
- **API Layer** (`api/`) - HTTP endpoints and routing
- **Service Layer** (`services/`) - Business logic and operations
- **Model Layer** (`models/`) - Database documents and schemas

## Requirements

- Python
- MongoDB
- Docker and Docker Compose

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd notes-api
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Update `.env` with your configuration:
```
DATABASE_NAME=notes_api
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRY=30
ENVIRONMENT=development
MONGODB_USER=admin
MONGODB_PASSWORD=secret
MONGODB_DATABASE=notes_api
```

4. Start the application:
```bash
docker-compose up --build
```

The API will be available at `http://127.0.0.1:8002`


## API Usage Examples

### 1. Create Organization

```bash
curl -X POST "http://127.0.0.1:8002/organizations/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Blutech LLC"}'
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "507f1f77bcf86cd799439011",
    "name": "Blutech LLC",
    "created_at": "2024-01-01T12:00:00Z"
  },
  "message": "Organization created successfully"
}
```

### 2. Create User
The first user created in each organization is automatically assigned the `admin` role, regardless of the role specified in the request.

```bash
curl -X POST "http://127.0.0.1:8002/organizations/69001235df940e56abd60b72/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "role": "writer"
  }'
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "507f191e810c19729de860ea",
    "email": "user@example.com",
    "org_id": "507f1f77bcf86cd799439011",
    "role": "writer",
    "is_active": true,
    "created_at": "2024-01-01T12:00:00Z"
  },
  "message": "User created successfully"
}
```

### 3. Login

```bash
curl -X POST "http://127.0.0.1:8002/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

Response:
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "user": {
      "id": "507f191e810c19729de860ea",
      "email": "user@example.com",
      "org_id": "507f1f77bcf86cd799439011",
      "role": "writer",
      "is_active": true,
      "created_at": "2024-01-01T12:00:00Z"
    }
  },
  "message": "Login successful"
}
```

### 4. Create Note
Requires `writer` or `admin` role.

```bash
curl -X POST "http://127.0.0.1:8002/notes/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -d '{
    "title": "Meeting Notes",
    "content": "Discussion about Q1 goals..."
  }'
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "507f1f77bcf86cd799439012",
    "title": "Meeting Notes",
    "content": "Discussion about Q1 goals...",
    "author_id": "507f191e810c19729de860ea",
    "org_id": "507f1f77bcf86cd799439011",
    "created_at": "2024-01-01T12:10:00Z",
    "updated_at": "2024-01-01T12:10:00Z"
  },
  "message": "Note created successfully"
}
```

### 5. List Notes

```bash
curl -X GET "http://127.0.0.1:8002/notes/?limit=20&offset=0" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

Response:
```json
{
  "success": true,
  "data": {
    "notes": [
      {
        "id": "507f1f77bcf86cd799439012",
        "title": "Meeting Notes",
        "content": "Discussion about Q1 goals...",
        "author_id": "507f191e810c19729de860ea",
        "org_id": "507f1f77bcf86cd799439011",
        "created_at": "2024-01-01T12:10:00Z",
        "updated_at": "2024-01-01T12:10:00Z"
      }
    ],
    "total": 1
  }
}
```

### 6. Get Specific Note

```bash
curl -X GET "http://127.0.0.1:8002/notes/69001415df940e56abd60b77" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "507f1f77bcf86cd799439012",
    "title": "Meeting Notes",
    "content": "Discussion about Q1 goals...",
    "author_id": "507f191e810c19729de860ea",
    "org_id": "507f1f77bcf86cd799439011",
    "created_at": "2024-01-01T12:10:00Z",
    "updated_at": "2024-01-01T12:10:00Z"
  }
}
```

### 7. Delete Note (Admin Only)

```bash
curl -X DELETE "http://127.0.0.1:8002/notes/69001415df940e56abd60b77" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

Response:
```
HTTP 204 No Content
(Empty body)
```

## Roles and Permissions

| Role   | View Notes | Create Notes | Delete Notes |
|--------|-----------|--------------|--------------|
| reader | ✓         | ✗            | ✗            |
| writer | ✓         | ✓            | ✗            |
| admin  | ✓         | ✓            | ✓            |

## Multi-Tenancy

- Each organization operates as an independent tenant
- Users can only access data within their organization (first users for each org are assigned the `admin` role)
- Email addresses are unique per organization (not globally)
- Organizations are unique by name
- All queries are automatically filtered by organization ID from the JWT token
- Authentication is handled via custom middleware

## Password Requirements

- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 digit

## Testing

Run tests:
```bash
docker-compose -f docker-compose.test.yaml up -d
TEST_MONGODB_URL=mongodb://localhost:27019 pytest 
```

Stop test database:
```bash
docker-compose -f docker-compose.test.yaml down
```

## Project Structure

```
notes-api/
├── api/                    # HTTP endpoints
│   ├── organization.py
│   ├── user.py
│   ├── auth.py
│   └── note.py
├── services/               # Business logic
│   ├── organization.py
│   ├── user.py
│   ├── auth.py
│   └── note.py
├── models/                 # Database models
│   ├── organization.py
│   ├── user.py
│   └── note.py
├── schemas/                # Request/Response schemas
│   ├── requests.py
│   └── responses.py
├── core/                   # Core utilities
│   ├── config.py           # Settings
│   ├── database.py         # MongoDB connection
│   ├── security.py         # JWT and password hashing
│   ├── dependencies.py     # FastAPI dependencies
│   ├── middleware.py       # Custom middleware
│   └── exceptions.py       # Custom exceptions
├── tests/                  # Test files
├── main.py                 # Application entry point
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```