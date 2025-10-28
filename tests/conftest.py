import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient

from main import app
from models.organization import Organization
from models.user import User
from models.note import Note
from core.security import hash_password
import os


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    os.environ["MONGODB_URL"] = "mongodb://localhost:27019"
    os.environ["DATABASE_NAME"] = "test_notes_api"
    os.environ["SECRET_KEY"] = "testsecret"
    os.environ["JWT_ALGORITHM"] = "HS256"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"


@pytest.fixture(scope="function")
async def test_db():
    client = AsyncIOMotorClient("mongodb://localhost:27019")
    database = client.test_notes_api

    await init_beanie(
        database=database,
        document_models=[Organization, User, Note],
    )

    yield database

    await Organization.delete_all()
    await User.delete_all()
    await Note.delete_all()

    client.close()


@pytest.fixture
async def client(test_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_org(test_db):
    org = Organization(name="Test Organization")
    await org.insert()
    return org


@pytest.fixture
async def test_admin_user(test_db, test_org):
    user = User(
        email="admin@test.com",
        password=hash_password("Password123"),
        org_id=str(test_org.id),
        role="admin",
    )
    await user.insert()
    return user


@pytest.fixture
async def test_writer_user(test_db, test_org):
    user = User(
        email="writer@test.com",
        password=hash_password("Password123"),
        org_id=str(test_org.id),
        role="writer",
    )
    await user.insert()
    return user


@pytest.fixture
async def test_reader_user(test_db, test_org):
    user = User(
        email="reader@test.com",
        password=hash_password("Password123"),
        org_id=str(test_org.id),
        role="reader",
    )
    await user.insert()
    return user


@pytest.fixture
async def admin_token(client, test_org, test_admin_user):
    response = await client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "Password123",
            "org_id": str(test_org.id),
        },
    )
    return response.json()["data"]["access_token"]


@pytest.fixture
async def writer_token(client, test_org, test_writer_user):
    response = await client.post(
        "/auth/login",
        json={
            "email": "writer@test.com",
            "password": "Password123",
            "org_id": str(test_org.id),
        },
    )
    return response.json()["data"]["access_token"]


@pytest.fixture
async def reader_token(client, test_org, test_reader_user):
    response = await client.post(
        "/auth/login",
        json={
            "email": "reader@test.com",
            "password": "Password123",
            "org_id": str(test_org.id),
        },
    )
    return response.json()["data"]["access_token"]


@pytest.fixture
async def test_note(test_db, test_org, test_writer_user):
    note = Note(
        title="Test Note",
        content="Test content",
        author_id=str(test_writer_user.id),
        org_id=str(test_org.id),
    )
    await note.insert()
    return note
