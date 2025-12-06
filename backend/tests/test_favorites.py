import pytest

pytestmark = pytest.mark.asyncio


async def test_add_to_favorites_success(authenticated_client, product_id):
    response = await authenticated_client.post(f"/favorites/{product_id}")
    assert response.status_code == 201


async def test_add_duplicate_favorite(authenticated_client, product_id):
    await authenticated_client.post(f"/favorites/{product_id}")
    response = await authenticated_client.post(f"/favorites/{product_id}")
    assert response.status_code == 400


async def test_remove_from_favorites(authenticated_client, product_id):
    await authenticated_client.post(f"/favorites/{product_id}")
    response = await authenticated_client.delete(f"/favorites/{product_id}")
    assert response.status_code in (200, 204)


async def test_get_favorites(authenticated_client, product_id):
    await authenticated_client.post(f"/favorites/{product_id}")
    response = await authenticated_client.get("/favorites/")
    assert response.status_code == 200
    assert any(p["id"] == product_id for p in response.json())
