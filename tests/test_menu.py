"""Tests for menu endpoints: /v1/menu, /v1/menu/search, /v1/menu/items/{id}"""


# ── GET /v1/menu ──


def test_menu_returns_all_categories(client):
    r = client.get("/v1/menu")
    assert r.status_code == 200
    data = r.json()
    assert data["restaurant_name"] == "Fast X Food"
    assert data["branch_id"] == "branch-001"
    assert data["menu_period"] == "all"
    assert len(data["categories"]) == 9


def test_menu_items_are_lightweight(client):
    r = client.get("/v1/menu")
    item = r.json()["categories"][0]["items"][0]
    assert "id" in item
    assert "name" in item
    assert "basePrice" in item
    assert "available" in item
    assert "ingredients" not in item
    assert "macros" not in item


def test_menu_accepts_branch_id(client):
    r = client.get("/v1/menu", params={"branch_id": "branch-999"})
    assert r.status_code == 200
    assert r.json()["branch_id"] == "branch-999"


def test_menu_period_breakfast_filters_categories(client):
    r = client.get("/v1/menu", params={"menu_period": "breakfast"})
    assert r.status_code == 200
    cats = r.json()["categories"]
    cat_ids = [c["id"] for c in cats]
    assert "cat-breakfast" in cat_ids
    assert "cat-drinks" in cat_ids
    assert "cat-burgers" not in cat_ids


def test_menu_unavailable_item_marked_false(client):
    r = client.get("/v1/menu")
    for cat in r.json()["categories"]:
        for item in cat["items"]:
            if item["id"] == "item-milkshake":
                assert item["available"] is False
                return
    raise AssertionError("item-milkshake not found in menu")


# ── GET /v1/menu/categories ──


def test_categories_returns_all(client):
    r = client.get("/v1/menu/categories")
    assert r.status_code == 200
    data = r.json()
    assert len(data["categories"]) == 9
    cat = data["categories"][0]
    assert "id" in cat
    assert "name" in cat
    assert "item_count" in cat


def test_categories_breakfast_period(client):
    r = client.get("/v1/menu/categories", params={"menu_period": "breakfast"})
    data = r.json()
    cat_ids = [c["id"] for c in data["categories"]]
    assert "cat-breakfast" in cat_ids
    assert "cat-burgers" not in cat_ids


# ── GET /v1/menu/search ──


def test_search_includes_combos(client):
    r = client.get("/v1/menu/search", params={"keyword": "combo"})
    data = r.json()
    combo_names = [i["name"] for i in data["results"] if "combo" in i["name"].lower()]
    assert len(combo_names) > 0, "Combos should appear in search results"


def test_search_combos_filtered_by_allergens(client):
    r = client.get("/v1/menu/search", params={"exclude_allergens": "gluten"})
    data = r.json()
    for item in data["results"]:
        assert "gluten" not in item["allergens"], f"{item['name']} has gluten but passed filter"


def test_search_dietary_vegan(client):
    r = client.get("/v1/menu/search", params={"dietary_tag": "vegan"})
    data = r.json()
    for item in data["results"]:
        assert "dairy" not in item["allergens"], f"{item['name']} has dairy but passed vegan filter"
        assert "eggs" not in item["allergens"], f"{item['name']} has eggs but passed vegan filter"
        assert "pork" not in item["allergens"], f"{item['name']} has pork but passed vegan filter"


def test_search_dietary_vegetarian_excludes_chicken_nuggets(client):
    r = client.get("/v1/menu/search", params={"dietary_tag": "vegetarian"})
    data = r.json()
    names = [i["name"] for i in data["results"]]
    assert "Chicken Nuggets" not in names, "Chicken Nuggets should be excluded from vegetarian results"


def test_search_dietary_vegan_no_meat_id_exclusion(client):
    """Vegan filter uses allergens only, not meat ingredient IDs."""
    r = client.get("/v1/menu/search", params={"dietary_tag": "vegan"})
    data = r.json()
    for item in data["results"]:
        assert "dairy" not in item["allergens"]
        assert "eggs" not in item["allergens"]
        assert "pork" not in item["allergens"]


def test_search_by_keyword_burger(client):
    r = client.get("/v1/menu/search", params={"keyword": "burger"})
    assert r.status_code == 200
    data = r.json()
    assert data["result_count"] > 0
    for item in data["results"]:
        assert "burger" in item["name"].lower() or "burger" in item.get("description", "").lower()


def test_search_by_category(client):
    r = client.get("/v1/menu/search", params={"category": "Sides"})
    data = r.json()
    names = [i["name"] for i in data["results"]]
    assert "Classic Fries" in names
    assert "Loaded Cheese Fries" in names


def test_search_exclude_allergens(client):
    r = client.get("/v1/menu/search", params={"exclude_allergens": "gluten,dairy"})
    data = r.json()
    for item in data["results"]:
        assert "gluten" not in item["allergens"]
        assert "dairy" not in item["allergens"]


def test_search_max_calories(client):
    r = client.get("/v1/menu/search", params={"max_calories": 200})
    data = r.json()
    for item in data["results"]:
        assert item["calories"] <= 200


def test_search_max_price(client):
    r = client.get("/v1/menu/search", params={"max_price": 300})
    data = r.json()
    for item in data["results"]:
        assert item["price"] <= 300


def test_search_min_protein(client):
    r = client.get("/v1/menu/search", params={"min_protein": 20})
    data = r.json()
    for item in data["results"]:
        assert item["protein"] >= 20


def test_search_no_results_returns_empty(client):
    r = client.get("/v1/menu/search", params={"keyword": "sushi"})
    data = r.json()
    assert data["result_count"] == 0
    assert data["results"] == []


def test_search_dietary_vegetarian(client):
    r = client.get("/v1/menu/search", params={"dietary_tag": "vegetarian"})
    data = r.json()
    for item in data["results"]:
        assert "pork" not in item["allergens"]


# ── GET /v1/menu/items/{item_id} ──


def test_item_detail_classic_burger(client):
    r = client.get("/v1/menu/items/item-classic-smash-burger")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "item-classic-smash-burger"
    assert data["name"] == "Classic Smash Burger"
    assert data["basePrice"] == 799
    assert data["available"] is True
    assert data["is_combo"] is False
    assert len(data["allergens"]) > 0
    assert data["macros"]["calories"] > 0
    assert len(data["default_ingredients"]) > 0
    assert len(data["available_additions"]) > 0


def test_item_detail_has_correct_ingredient_structure(client):
    r = client.get("/v1/menu/items/item-classic-smash-burger")
    data = r.json()

    fixed = [i for i in data["default_ingredients"] if i["removable"] is False]
    assert len(fixed) >= 2

    leveled = [i for i in data["default_ingredients"] if i.get("levels")]
    assert len(leveled) >= 1

    for add in data["available_additions"]:
        assert "name" in add
        assert "price" in add


def test_item_detail_combo(client):
    r = client.get("/v1/menu/items/item-classic-combo")
    assert r.status_code == 200
    data = r.json()
    assert data["is_combo"] is True
    assert len(data["combo_items"]) == 3
    assert data["savings_vs_individual"] > 0
    for ci in data["combo_items"]:
        assert "item_id" in ci
        assert "label" in ci


def test_item_detail_sized_item(client):
    r = client.get("/v1/menu/items/item-chicken-nuggets")
    assert r.status_code == 200
    data = r.json()
    assert data["basePrice"] == 0
    assert len(data["sizes"]) == 3
    assert len(data["choices"]) == 1
    assert data["choices"][0]["name"] == "Dipping Sauce"


def test_item_detail_not_found(client):
    r = client.get("/v1/menu/items/item-nonexistent")
    assert r.status_code == 404
    assert r.json()["error"] == "Item not found"


def test_item_detail_unavailable_item(client):
    r = client.get("/v1/menu/items/item-milkshake")
    assert r.status_code == 200
    assert r.json()["available"] is False
