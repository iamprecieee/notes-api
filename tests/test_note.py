import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_note_as_writer(client: AsyncClient, writer_token):
    response = await client.post(
        "/notes/",
        json={"title": "Test Note", "content": "Test content"},
        headers={"Authorization": f"Bearer {writer_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Test Note"
    assert data["data"]["content"] == "Test content"


@pytest.mark.asyncio
async def test_create_note_as_admin(client: AsyncClient, admin_token):
    response = await client.post(
        "/notes/",
        json={"title": "Admin Note", "content": "Admin content"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_create_note_as_reader_fails(client: AsyncClient, reader_token):
    response = await client.post(
        "/notes/",
        json={"title": "Reader Note", "content": "Should fail"},
        headers={"Authorization": f"Bearer {reader_token}"},
    )

    assert response.status_code == 403
    data = response.json()
    assert data["success"] is False


@pytest.mark.asyncio
async def test_list_notes(client: AsyncClient, reader_token, test_note):
    response = await client.get(
        "/notes/",
        headers={"Authorization": f"Bearer {reader_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "notes" in data["data"]
    assert data["data"]["total"] >= 1


@pytest.mark.asyncio
async def test_get_note(client: AsyncClient, reader_token, test_note):
    response = await client.get(
        f"/notes/{test_note.id}",
        headers={"Authorization": f"Bearer {reader_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Test Note"


@pytest.mark.asyncio
async def test_delete_note_as_admin(client: AsyncClient, admin_token, test_note):
    response = await client.delete(
        f"/notes/{test_note.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 204
    assert response.content == b""


@pytest.mark.asyncio
async def test_delete_note_as_writer_fails(
    client: AsyncClient, writer_token, test_note
):
    response = await client.delete(
        f"/notes/{test_note.id}",
        headers={"Authorization": f"Bearer {writer_token}"},
    )

    assert response.status_code == 403
    data = response.json()
    assert data["success"] is False


@pytest.mark.asyncio
async def test_delete_note_as_reader_fails(
    client: AsyncClient, reader_token, test_note
):
    response = await client.delete(
        f"/notes/{test_note.id}",
        headers={"Authorization": f"Bearer {reader_token}"},
    )

    assert response.status_code == 403
    data = response.json()
    assert data["success"] is False


@pytest.mark.asyncio
async def test_unauthenticated_access_fails(client: AsyncClient):
    response = await client.get("/notes/")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_cross_organization_access_prevented(
    client: AsyncClient, writer_token, test_db
):
    from models.organization import Organization
    from models.user import User
    from models.note import Note
    from core.security import hash_password

    other_org = Organization(name="Other Org")
    await other_org.insert()

    other_user = User(
        email="other@test.com",
        password=hash_password("Password123"),
        org_id=str(other_org.id),
        role="writer",
    )
    await other_user.insert()

    other_note = Note(
        title="Other Note",
        content="Other content",
        author_id=str(other_user.id),
        org_id=str(other_org.id),
    )
    await other_note.insert()

    response = await client.get(
        f"/notes/{other_note.id}",
        headers={"Authorization": f"Bearer {writer_token}"},
    )

    assert response.status_code == 404
