"""Tests for /v1/availability/{item_id}"""


def test_available_item(client):
    r = client.get("/v1/availability/item-classic-smash-burger")
    assert r.status_code == 200
    data = r.json()
    assert data["item_id"] == "item-classic-smash-burger"
    assert data["available"] is True
    assert "reason" not in data


def test_unavailable_summer_bbq_burger(client):
    r = client.get("/v1/availability/item-summer-bbq-burger")
    assert r.status_code == 200
    data = r.json()
    assert data["available"] is False
    assert "reason" in data
    assert "summer bbq burger" in data["reason"].lower()


def test_unavailable_mac_and_cheese(client):
    r = client.get("/v1/availability/item-mac-and-cheese")
    assert r.status_code == 200
    data = r.json()
    assert data["available"] is False
    assert "mac" in data["reason"].lower()


def test_unknown_item_is_available(client):
    r = client.get("/v1/availability/item-doesnt-exist")
    assert r.status_code == 200
    assert r.json()["available"] is True
