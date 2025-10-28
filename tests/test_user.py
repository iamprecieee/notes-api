import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, test_org):
    response = await client.post(
        f"/organizations/{test_org.id}/users/",
        json={
            "email": "newuser@test.com",
            "password": "Password123",
            "role": "writer",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "newuser@test.com"
    assert data["data"]["role"] == "admin"
    assert data["data"]["is_active"] is True

    response = await client.post(
        f"/organizations/{test_org.id}/users/",
        json={
            "email": "newuser1@test.com",
            "password": "Password123",
            "role": "writer",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "newuser1@test.com"
    assert data["data"]["role"] == "writer"
    assert data["data"]["is_active"] is True


@pytest.mark.asyncio
async def test_create_duplicate_user_in_same_org_fails(
    client: AsyncClient, test_org, test_admin_user
):
    response = await client.post(
        f"/organizations/{test_org.id}/users/",
        json={
            "email": "admin@test.com",
            "password": "Password123",
            "role": "writer",
        },
    )

    assert response.status_code == 409
    data = response.json()
    assert data["success"] is False


@pytest.mark.asyncio
async def test_create_same_email_in_different_org_succeeds(
    client: AsyncClient, test_db
):
    from models.organization import Organization

    org1 = Organization(name="Org 1")
    await org1.insert()

    org2 = Organization(name="Org 2")
    await org2.insert()

    response1 = await client.post(
        f"/organizations/{org1.id}/users/",
        json={
            "email": "shared@test.com",
            "password": "Password123",
            "role": "writer",
        },
    )
    assert response1.status_code == 200

    response2 = await client.post(
        f"/organizations/{org2.id}/users/",
        json={
            "email": "shared@test.com",
            "password": "Password123",
            "role": "reader",
        },
    )
    assert response2.status_code == 200


@pytest.mark.asyncio
async def test_create_user_invalid_role(client: AsyncClient, test_org):
    response = await client.post(
        f"/organizations/{test_org.id}/users/",
        json={
            "email": "invalid@test.com",
            "password": "Password123",
            "role": "superadmin",
        },
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_user_short_password(client: AsyncClient, test_org):
    response = await client.post(
        f"/organizations/{test_org.id}/users/",
        json={
            "email": "short@test.com",
            "password": "Pass1",
            "role": "writer",
        },
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_user_nonexistent_org(client: AsyncClient):
    response = await client.post(
        "/organizations/507f1f77bcf86cd799439011/users/",
        json={
            "email": "user@test.com",
            "password": "Password123",
            "role": "writer",
        },
    )

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
