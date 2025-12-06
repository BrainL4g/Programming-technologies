import pytest

pytestmark = pytest.mark.asyncio


async def test_price_changes_report(client):
    response = await client.get("/reports/price-changes/")
    assert response.status_code == 200


async def test_availability_report(client):
    response = await client.get("/reports/availability/")
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "available" in data


async def test_sync_status_report(client):
    response = await client.get("/reports/sync-status/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
