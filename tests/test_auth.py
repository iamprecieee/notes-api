import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_org, test_admin_user):
    response = await client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "Password123",
            "org_id": str(test_org.id),
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"
    assert data["data"]["user"]["email"] == "admin@test.com"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_org, test_admin_user):
    response = await client.post(
        "/auth/login",
        json={
            "email": "admin@test.com",
            "password": "WrongPassword",
            "org_id": str(test_org.id),
        },
    )

    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient, test_org):
    response = await client.post(
        "/auth/login",
        json={
            "email": "nonexistent@test.com",
            "password": "Password123",
            "org_id": str(test_org.id),
        },
    )

    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
