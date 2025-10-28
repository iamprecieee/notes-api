from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from core.config import get_settings

_client: AsyncIOMotorClient | None = None


async def connect_to_database():
    global _client

    settings = get_settings()

    _client = AsyncIOMotorClient(settings.mongodb_url)
    database = _client.get_database(settings.database_name)

    from models.organization import Organization
    from models.user import User
    from models.note import Note

    await init_beanie(
        database=database,
        document_models=[Organization, User, Note],
    )


async def close_database_connection():
    global _client

    if _client:
        _client.close()
        _client = None
