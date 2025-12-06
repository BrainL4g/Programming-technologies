import pytest

pytestmark = pytest.mark.asyncio


async def test_create_offer_and_price_history(admin_client, store_id):
    data = {
        "external_id": "123",
        "product_name": "iPhone 16",
        "store_id": str(store_id),
        "price": 120000.0,
        "url": "https://example.com/123",
    }

    resp = await admin_client.post("/offers/", json=data)
    assert resp.status_code == 201

    offer_id = resp.json()["id"]

    await admin_client.patch(
        f"/offers/{offer_id}",
        json={"price": 115000.0},
    )

    history = await admin_client.get(
        f"/offers/{offer_id}/price-history/"
    )
    assert history.status_code == 200
    assert len(history.json()) == 2


async def test_offer_filters(admin_client, client, store_id):
    await admin_client.post("/offers/", json={
        "external_id": "a1",
        "product_name": "MacBook",
        "store_id": str(store_id),
        "price": 200000,
        "available": True,
        "url": "https://a.com",
    })

    await admin_client.post("/offers/", json={
        "external_id": "a2",
        "product_name": "ThinkPad",
        "store_id": str(store_id),
        "price": 150000,
        "available": False,
        "url": "https://b.com",
    })

    resp = await client.get("/offers/?available=true")
    assert all(o["available"] for o in resp.json())

    resp = await client.get("/offers/?min_price=180000")
    assert all(o["price"] >= 180000 for o in resp.json())
