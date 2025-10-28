from pydantic import BaseModel, EmailStr, Field


class CreateOrganizationRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = Field(..., pattern="^(reader|writer|admin)$")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CreateNoteRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class UpdateNoteRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    content: str | None = Field(None, min_length=1)
