from datetime import datetime, timezone

from beanie import Document, Indexed
from pydantic import Field


class Note(Document):
    title: str
    content: str
    author_id: Indexed(str)
    org_id: Indexed(str)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "notes"
