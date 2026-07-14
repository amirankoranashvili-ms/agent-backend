"""Tests for POST /v1/orders/submit"""

BASIC_ORDER = {
    "items": [
        {"id": "item-classic-smash-burger", "name": "Classic Smash Burger", "quantity": 1, "unit_price": 799, "total_price": 799, "calories": 565},
    ],
    "subtotal": 799,
}


def test_submit_valid_order(client):
    r = client.post("/v1/orders/submit", json=BASIC_ORDER)
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert data["order_number"].startswith("DT-")
    assert data["subtotal"] == 799
    assert data["promo_discount"] == 0
    assert data["tax"] == round(799 * 0.085)
    assert data["total_with_tax"] == 799 + data["tax"]
    assert data["total_display"].startswith("$")
    assert 3 <= data["estimated_wait_minutes"] <= 8
    assert data["loyalty_points_earned"] == 0


def test_submit_with_promo_save10(client):
    order = {**BASIC_ORDER, "promo_code": "SAVE10"}
    r = client.post("/v1/orders/submit", json=order)
    data = r.json()
    assert data["success"] is True
    assert data["promo_discount"] == 79  # 10% of 799
    expected_after_promo = 799 - 79
    assert data["tax"] == round(expected_after_promo * 0.085)
    assert data["total_with_tax"] == expected_after_promo + data["tax"]


def test_submit_with_promo_freefries(client):
    order = {
        "items": [
            {"id": "item-classic-smash-burger", "name": "Classic Smash Burger", "quantity": 1, "unit_price": 799, "total_price": 799},
            {"id": "item-classic-fries", "name": "Classic Fries", "quantity": 1, "unit_price": 349, "total_price": 349},
        ],
        "subtotal": 1148,
        "promo_code": "FREEFRIES",
    }
    r = client.post("/v1/orders/submit", json=order)
    data = r.json()
    assert data["success"] is True
    assert data["promo_discount"] == 399  # medium fries price


def test_submit_with_promo_freefries_no_fries_in_order(client):
    order = {**BASIC_ORDER, "promo_code": "FREEFRIES"}
    r = client.post("/v1/orders/submit", json=order)
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert data["promo_discount"] == 0


def test_submit_with_promo_combo5_valid(client):
    order = {
        "items": [
            {"id": "item-classic-combo", "name": "Classic Combo", "quantity": 1, "unit_price": 1199, "total_price": 1199},
        ],
        "subtotal": 1199,
        "promo_code": "COMBO5",
    }
    r = client.post("/v1/orders/submit", json=order)
    data = r.json()
    assert data["success"] is True
    assert data["promo_discount"] == 500


def test_submit_with_promo_combo5_no_combo(client):
    order = {**BASIC_ORDER, "promo_code": "COMBO5"}
    r = client.post("/v1/orders/submit", json=order)
    assert r.status_code == 400
    assert r.json()["success"] is False
    assert "combo" in r.json()["error"].lower()


def test_submit_invalid_promo(client):
    order = {**BASIC_ORDER, "promo_code": "BADCODE"}
    r = client.post("/v1/orders/submit", json=order)
    assert r.status_code == 400
    data = r.json()
    assert data["success"] is False
    assert data["error"] == "Invalid promo code"
    assert data["promo_code"] == "BADCODE"


def test_submit_with_loyalty_earns_points(client):
    order = {**BASIC_ORDER, "loyalty_customer_id": "loyalty-001"}
    r = client.post("/v1/orders/submit", json=order)
    data = r.json()
    assert data["loyalty_points_earned"] > 0
    assert data["loyalty_points_earned"] == data["total_with_tax"] // 100


def test_submit_with_notes(client):
    order = {**BASIC_ORDER, "notes": ["extra napkins", "no straw"]}
    r = client.post("/v1/orders/submit", json=order)
    data = r.json()
    assert data["notes"] == ["extra napkins", "no straw"]


def test_submit_promo_case_insensitive(client):
    order = {**BASIC_ORDER, "promo_code": "save10"}
    r = client.post("/v1/orders/submit", json=order)
    assert r.json()["success"] is True
    assert r.json()["promo_discount"] == 79
