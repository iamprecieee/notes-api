from datetime import datetime
from typing import Any, List

from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    data: Any
    message: str | None = None


class OrganizationResponse(BaseModel):
    id: str
    name: str
    created_at: datetime


class UserResponse(BaseModel):
    id: str
    email: str
    org_id: str
    role: str
    is_active: bool
    created_at: datetime


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    org_id: str
    created_at: datetime
    updated_at: datetime


class NoteListResponse(BaseModel):
    notes: List[NoteResponse]
    total: int
