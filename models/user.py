from datetime import datetime, timezone

from beanie import Document, Indexed
from pydantic import Field, EmailStr
from pymongo import IndexModel


class User(Document):
    email: EmailStr
    password: str
    org_id: Indexed(str)
    role: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"
        indexes = [IndexModel([("email", 1), ("org_id", 1)], unique=True)]
