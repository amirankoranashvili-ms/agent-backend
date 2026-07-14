"""Tests for health, kitchen wait-time, feedback, and escalation endpoints"""


# ── GET /health ──


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ── GET /v1/promo/validate ──


def test_promo_valid(client):
    r = client.get("/v1/promo/validate", params={"code": "SAVE10"})
    assert r.status_code == 200
    data = r.json()
    assert data["valid"] is True
    assert data["code"] == "SAVE10"
    assert data["type"] == "percent"
    assert "description" in data


def test_promo_valid_case_insensitive(client):
    r = client.get("/v1/promo/validate", params={"code": "save10"})
    assert r.json()["valid"] is True
    assert r.json()["code"] == "SAVE10"


def test_promo_invalid(client):
    r = client.get("/v1/promo/validate", params={"code": "BADCODE"})
    assert r.status_code == 200
    data = r.json()
    assert data["valid"] is False
    assert data["code"] == "BADCODE"
    assert "type" not in data


# ── GET /v1/kitchen/wait-time ──


def test_wait_time(client):
    r = client.get("/v1/kitchen/wait-time")
    assert r.status_code == 200
    data = r.json()
    assert data["available"] is True
    assert 2 <= data["estimated_minutes"] <= 10
    assert 1 <= data["queue_depth"] <= 6


def test_wait_time_varies(client):
    results = set()
    for _ in range(20):
        r = client.get("/v1/kitchen/wait-time")
        results.add(r.json()["estimated_minutes"])
    assert len(results) > 1


# ── POST /v1/feedback ──


def test_feedback(client):
    r = client.post("/v1/feedback", json={
        "branch_id": "branch-001",
        "session_id": "sess-abc123",
        "type": "complaint",
        "text": "The fries were cold last time.",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["logged"] is True
    assert data["feedback_id"].startswith("fb-")
    assert data["message"] == "Thank you for your feedback."


def test_feedback_minimal(client):
    r = client.post("/v1/feedback", json={})
    assert r.status_code == 200
    assert r.json()["logged"] is True


# ── POST /v1/escalation ──


def test_escalation(client):
    r = client.post("/v1/escalation", json={
        "session_id": "sess-abc123",
        "branch_id": "branch-001",
        "reason": "allergy_safety",
        "summary": "Customer has severe peanut allergy.",
        "order_state": [{"name": "Classic Burger", "qty": 1}],
        "order_subtotal": 1598,
        "loyalty_customer": {"name": "Sarah", "id": "loyalty-001"},
        "promo_code": "",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["acknowledged"] is True
    assert data["escalation_id"].startswith("esc-")
    assert data["message"] == "Escalation received. Routing to staff."


def test_escalation_minimal(client):
    r = client.post("/v1/escalation", json={})
    assert r.status_code == 200
    assert r.json()["acknowledged"] is True
