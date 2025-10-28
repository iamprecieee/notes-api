from datetime import datetime, timezone

from beanie import Document
from beanie.odm.fields import Indexed
from pydantic import Field


class Organization(Document):
    name: Indexed(str, unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "organizations"
