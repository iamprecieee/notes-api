from datetime import datetime, timezone

from beanie import Document
from pydantic import Field


class Organization(Document):
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "organizations"
