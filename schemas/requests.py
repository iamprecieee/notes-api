from pydantic import BaseModel, EmailStr, Field, field_validator

from core.exceptions import ValidationError


class CreateOrganizationRequest(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if 100 < len(value) < 1:
            raise ValidationError(
                detail="Organization name must be at within 1 to 100 characters"
            )

        return value


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    role: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValidationError(detail="Password must be at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValidationError(
                detail="Password must contain at least 1 uppercase letter"
            )
        if not any(c.isdigit() for c in value):
            raise ValidationError(detail="Password must contain at least 1 digit")

        return value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        if value not in ["reader", "writer", "admin"]:
            raise ValidationError(
                detail="Invalid role. Must be reader, writer, or admin"
            )

        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CreateNoteRequest(BaseModel):
    title: str
    content: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if 200 < len(value) < 1:
            raise ValidationError(
                detail="Note title must be at within 1 to 200 characters"
            )

        return value

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        if len(value) < 1:
            raise ValidationError(detail="Note content must be at least 1 character")

        return value
