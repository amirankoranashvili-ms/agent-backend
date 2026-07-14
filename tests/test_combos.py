"""Tests for POST /v1/combos/check"""


def test_combo_found_classic(client):
    r = client.post("/v1/combos/check", json={
        "item_ids": ["item-classic-smash-burger", "item-classic-fries", "item-fountain-drink"],
    })
    assert r.status_code == 200
    data = r.json()
    assert data["combo_available"] is True
    assert len(data["combos"]) >= 1
    combo = data["combos"][0]
    assert combo["combo_id"] == "item-classic-combo"
    assert combo["combo_price"] == 1199
    assert combo["savings"] > 0
    assert combo["individual_total"] > combo["combo_price"]


def test_combo_not_found(client):
    r = client.post("/v1/combos/check", json={
        "item_ids": ["item-classic-fries", "item-onion-rings"],
    })
    assert r.status_code == 200
    data = r.json()
    assert data["combo_available"] is False
    assert data["combos"] == []


def test_combo_superset_still_matches(client):
    r = client.post("/v1/combos/check", json={
        "item_ids": [
            "item-classic-smash-burger",
            "item-classic-fries",
            "item-fountain-drink",
            "item-onion-rings",
        ],
    })
    data = r.json()
    assert data["combo_available"] is True
    combo_ids = [c["combo_id"] for c in data["combos"]]
    assert "item-classic-combo" in combo_ids


def test_combo_empty_list(client):
    r = client.post("/v1/combos/check", json={"item_ids": []})
    assert r.status_code == 200
    assert r.json()["combo_available"] is False
