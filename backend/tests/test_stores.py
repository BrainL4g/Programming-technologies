import pytest

pytestmark = pytest.mark.asyncio


async def test_create_store(admin_client):
    response = await admin_client.post(
        "/stores/",
        json={"name": "DNS", "domain": "dns-shop.ru"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "DNS"


async def test_get_stores_list(client):
    response = await client.get("/stores/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_update_store(admin_client, store_id):
    response = await admin_client.put(
        f"/stores/{store_id}",
        json={"name": "DNS Updated"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "DNS Updated"


async def test_delete_store(admin_client, store_id):
    response = await admin_client.delete(f"/stores/{store_id}")
    assert response.status_code == 204
