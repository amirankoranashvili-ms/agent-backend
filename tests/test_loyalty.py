"""Tests for loyalty endpoints: lookup, orders, redeem"""


# ── GET /v1/loyalty/lookup ──


def test_lookup_by_phone(client):
    r = client.get("/v1/loyalty/lookup", params={"identifier": "555-0101", "type": "phone"})
    assert r.status_code == 200
    data = r.json()
    assert data["found"] is True
    assert data["name"] == "Sarah"
    assert data["id"] == "loyalty-001"
    assert data["points_balance"] == 2450
    assert len(data["available_rewards"]) == 2
    assert len(data["usual_order"]) == 3


def test_lookup_by_loyalty_id(client):
    r = client.get("/v1/loyalty/lookup", params={"identifier": "loyalty-002", "type": "loyalty_id"})
    data = r.json()
    assert data["found"] is True
    assert data["name"] == "Marcus"


def test_lookup_by_qr(client):
    r = client.get("/v1/loyalty/lookup", params={"identifier": "loyalty-003", "type": "qr"})
    data = r.json()
    assert data["found"] is True
    assert data["name"] == "Emily"


def test_lookup_not_found(client):
    r = client.get("/v1/loyalty/lookup", params={"identifier": "555-9999", "type": "phone"})
    assert r.status_code == 200
    data = r.json()
    assert data["found"] is False
    assert "message" in data


def test_lookup_missing_identifier(client):
    r = client.get("/v1/loyalty/lookup")
    assert r.status_code == 422


# ── GET /v1/loyalty/{customer_id}/orders ──


def test_orders_returns_history(client):
    r = client.get("/v1/loyalty/loyalty-001/orders")
    assert r.status_code == 200
    data = r.json()
    assert data["customer_id"] == "loyalty-001"
    assert len(data["orders"]) >= 2
    order = data["orders"][0]
    assert "order_id" in order
    assert "date" in order
    assert "items" in order
    assert "total" in order


def test_orders_limit(client):
    r = client.get("/v1/loyalty/loyalty-001/orders", params={"limit": 1})
    assert len(r.json()["orders"]) == 1


def test_orders_not_found(client):
    r = client.get("/v1/loyalty/loyalty-999/orders")
    assert r.status_code == 404
    assert r.json()["error"] == "Customer not found"


# ── POST /v1/loyalty/{customer_id}/redeem ──


def test_redeem_free_drink(client):
    r = client.post("/v1/loyalty/loyalty-001/redeem", json={
        "reward_id": "reward-free-drink",
        "order_subtotal": 1847,
    })
    assert r.status_code == 200
    data = r.json()
    assert data["applied"] is True
    assert data["reward_name"] == "Free Medium Drink"
    assert data["discount_cents"] == 249
    assert data["new_subtotal"] == 1598


def test_redeem_2off_combo(client):
    r = client.post("/v1/loyalty/loyalty-001/redeem", json={
        "reward_id": "reward-2off-combo",
        "order_subtotal": 1199,
    })
    data = r.json()
    assert data["applied"] is True
    assert data["discount_cents"] == 200
    assert data["new_subtotal"] == 999


def test_redeem_invalid_reward(client):
    r = client.post("/v1/loyalty/loyalty-002/redeem", json={
        "reward_id": "reward-free-drink",
        "order_subtotal": 1000,
    })
    assert r.status_code == 400
    assert r.json()["applied"] is False


def test_redeem_unknown_customer(client):
    r = client.post("/v1/loyalty/loyalty-999/redeem", json={
        "reward_id": "reward-free-drink",
        "order_subtotal": 1000,
    })
    assert r.status_code == 400


def test_redeem_discount_doesnt_go_negative(client):
    r = client.post("/v1/loyalty/loyalty-001/redeem", json={
        "reward_id": "reward-free-drink",
        "order_subtotal": 100,
    })
    data = r.json()
    assert data["new_subtotal"] == 0
