import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_organization(client: AsyncClient):
    response = await client.post(
        "/organizations/",
        json={"name": "Test Corp"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Test Corp"
    assert "id" in data["data"]
    assert "created_at" in data["data"]

    response2 = await client.post(
        "/organizations/",
        json={"name": "Test Corp"},
    )

    assert response2.status_code == 409
