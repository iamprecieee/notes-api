## Overview

Multi-tenant Notes API where organizations manage users and notes independently. Users have roles that control their permissions. Built with FastAPI and MongoDB.

## Architecture

Three-layer architecture with clear separation:

```
api/          - HTTP endpoints and routing
services/     - Business logic and operations
models/       - Database documents and schemas
```

## Project Structure

```
notes-api/
├── api/
│   ├── organizations.py
│   ├── users.py
│   ├── auth.py
│   └── notes.py
├── services/
│   ├── organization_service.py
│   ├── user_service.py
│   ├── auth_service.py
│   └── note_service.py
├── models/
│   ├── organization.py
│   ├── user.py
│   └── note.py
├── schemas/
│   ├── requests.py
│   └── responses.py
├── core/
│   ├── config.py
│   ├── database.py
│   ├── security.py
│   ├── dependencies.py
│   └── exceptions.py
├── tests/
│   ├── conftest.py
│   ├── test_organizations.py
│   ├── test_users.py
│   ├── test_auth.py
│   └── test_notes.py
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── main.py
├── pyproject.toml
└── README.md
```

## Data Models

### Organization
```python
id: ObjectId
name: str
created_at: datetime
```

### User
```python
id: ObjectId
email: str              
password: str           
org_id: ObjectId
role: str              
is_active: bool
created_at: datetime

Indexes:
- Compound unique: (email, org_id)
- Single: org_id
```

### Note
```python
id: ObjectId
title: str
content: str
author_id: ObjectId
org_id: ObjectId
created_at: datetime
updated_at: datetime

Indexes:
- Single: org_id
- Single: author_id
```

## API Endpoints

### Organizations
```
POST /organizations/
- Create organization
- Public (no auth)
- Body: { name }
- Returns: { id, name, created_at }
```

### Users
```
POST /organizations/{org_id}/users/
- Create user in organization
- Public (no auth)
- Body: { email, password, role }
- Returns: { id, email, org_id, role, created_at }
```

### Authentication
```
POST /auth/login
- Login user
- Public (no auth)
- Body: { email, password }
- Returns: { access_token, token_type, user }
```

### Notes
```
POST /notes/
- Create note
- Requires: JWT, writer or admin role
- Body: { title, content }
- Returns: { id, title, content, author_id, org_id, created_at }

GET /notes/
- List organization notes
- Requires: JWT, any role
- Query: limit, offset
- Returns: { notes: [...], total }

GET /notes/{id}
- Get specific note
- Requires: JWT, any role, same org
- Returns: { id, title, content, author_id, org_id, created_at, updated_at }

DELETE /notes/{id}
- Delete note
- Requires: JWT, admin role, same org
- Returns: { success: true }
```

## Multi-Tenancy

Every request for notes/users includes org_id filtering:

```python
# From JWT token
user_org_id = current_user.org_id

# Query always filters by org
notes = await Note.find(Note.org_id == user_org_id).to_list()
```

Users cannot access data from other organizations. All database queries must filter by `org_id`.

## Roles and Permissions

Three roles with specific permissions:

**Reader:**
- View notes

**Writer:**
- View notes
- Create notes

**Admin:**
- View notes
- Create notes
- Delete notes

## Authentication Flow

### User Registration
1. Client: POST /organizations/{org_id}/users/
2. Server validates organization exists
3. Server checks email unique within organization
4. Password hashed with bcrypt
5. User created with specified role (first user in each org is given the admin role)
6. Returns user data (not logged in)
    ```json
    {
        "role": "writer",
        "email": "user@example.com"
    }
    ```

### User Login
1. Client: POST /auth/login with email, password
2. Server finds user by email
3. Password verified
4. JWT generated with payload:
   ```json
   {
     "user_id": "507f1f77bcf86cd799439011",
     "org_id": "507f191e810c19729de860ea",
     "role": "writer",
     "email": "user@example.com",
     "exp": 1234567890
   }
   ```
5. Returns token and user data

### Request Authorization
1. Client includes header: `Authorization: Bearer {token}`
2. Server extracts and validates token
3. Token payload becomes current_user
4. Route handler checks role permissions
5. All queries filtered by user's org_id

## Security

### Password Security
- Bcrypt hashing with cost factor 12
- Minimum 8 characters
- Never stored in JWT or returned in responses

### Token Security
- JWT signed with HS256
- 30 minute expiration
- Contains: `user_id`, `org_id`, `role`, `email`
- Validated on every request

### Data Isolation
- All queries filter by `org_id` from JWT
- Users cannot access other organizations
- `ObjectId` validated before queries


## Implementation Steps

### Day 1: Foundation and Organizations
1. Setup project structure
2. Configure MongoDB connection
3. Create Organization model
4. Create Organization service
5. Create Organization endpoints
6. Basic tests

### Day 2: Users and Authentication
1. Create User model with org_id
2. Create password hashing utilities
3. Create User service
4. Create user registration endpoint
5. Create JWT utilities
6. Create Auth service
7. Create login endpoint
8. Create authentication dependency
9. User and auth tests

### Day 3: Notes and Testing
1. Create Note model with org_id
2. Create Note service with permission checks
3. Create Note endpoints
4. Multi-tenant isolation tests
5. Permission tests for all roles
6. Docker setup
7. Documentation

## Key Implementation Points

### Beanie Document Pattern
```python
class User(Document):
    email: str
    org_id: str
    
    class Settings:
        name = "users"
        indexes = [
            [("email", 1), ("org_id", 1)]
        ]
```

### Service Pattern
```python
class UserService:
    async def create_user(self, email, password, org_id, role):
        # Validate org exists
        org = await Organization.get(org_id)
        if not org:
            raise NotFoundError("Organization not found")
        
        # Check email unique in org
        existing = await User.find_one(
            User.email == email,
            User.org_id == org_id
        )
        if existing:
            raise ConflictError("Email exists in organization")
        
        # Hash password
        hashed = hash_password(password)
        
        # Create user
        user = User(
            email=email,
            password=hashed,
            org_id=org_id,
            role=role
        )
        await user.insert()
        return user
```

### Router Pattern
```python
@router.post("/organizations/{org_id}/users/")
async def create_user(
    org_id: str,
    request: CreateUserRequest,
    service: UserService = Depends(get_user_service)
):
    user = await service.create_user(
        email=request.email,
        password=request.password,
        org_id=org_id,
        role=request.role
    )
    return {"success": True, "data": user}
```

## Error Handling

### Custom Exceptions
```python
class NotFoundError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class ConflictError(Exception):
    pass
```

### Exception Handlers
```python
@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"success": False, "message": str(exc)}
    )

@app.exception_handler(ForbiddenError)
async def forbidden_handler(request, exc):
    return JSONResponse(
        status_code=403,
        content={"success": False, "message": str(exc)}
    )
```

## Success Criteria

Implementation complete when:
- Organizations can be created
- Users can be created per organization with email scoped to org
- Users can login and receive JWT
- Notes can be created by writers and admins
- All users can view notes in their organization
- Only admins can delete notes
- Users cannot access other organizations data
- Tests verify multi-tenancy and permissions
- Docker setup works
- README has clear setup instructions