import json
from pathlib import Path

from mock_data import UNAVAILABLE_ITEMS

_MENU: dict = {}
_INGREDIENT_LIB: dict = {}
_ITEMS_BY_ID: dict = {}

MEAT_INGREDIENT_IDS = {
    "ing-beef-patty",
    "ing-double-beef-patty",
    "ing-extra-patty",
    "ing-fried-chicken-breast",
    "ing-grilled-chicken-breast",
    "ing-sausage-patty",
}

DIETARY_EXCLUSIONS = {
    "gluten-free": {"allergens": {"gluten"}},
    "dairy-free": {"allergens": {"dairy"}},
    "vegan": {"allergens": {"dairy", "eggs", "pork"}},
    "vegetarian": {"allergens": {"pork"}, "ingredient_ids": MEAT_INGREDIENT_IDS},
}


def load_menu():
    global _MENU, _INGREDIENT_LIB, _ITEMS_BY_ID
    menu_path = Path(__file__).parent / "sample_menu.json"
    if not menu_path.exists():
        menu_path = Path(__file__).parent.parent / "sample_menu.json"
    with open(menu_path) as f:
        _MENU = json.load(f)
    _INGREDIENT_LIB = _MENU.get("ingredientLibrary", {})
    _ITEMS_BY_ID = {}
    for cat in _MENU.get("categories", []):
        for item in cat.get("items", []):
            _ITEMS_BY_ID[item["id"]] = item


def get_menu():
    return _MENU


def get_ingredient_library():
    return _INGREDIENT_LIB


def get_item_by_id(item_id: str) -> dict | None:
    return _ITEMS_BY_ID.get(item_id)


def get_all_items() -> list[dict]:
    return list(_ITEMS_BY_ID.values())


def is_available(item_id: str) -> bool:
    return item_id not in UNAVAILABLE_ITEMS


def resolve_default_ingredients(item: dict) -> tuple[set, dict, list[dict]]:
    allergens: set[str] = set()
    macros = {"cal": 0, "fat": 0, "protein": 0, "carbs": 0}
    default_ings = []
    for ing in item.get("ingredients", []):
        if not ing.get("default", False):
            continue
        lib_entry = _INGREDIENT_LIB.get(ing.get("id", ""), {})
        for a in lib_entry.get("allergens", []):
            allergens.add(a)
        for key in macros:
            macros[key] += lib_entry.get("macros", {}).get(key, 0)
        default_ings.append(ing)

    if not default_ings:
        for a in item.get("allergens", []):
            allergens.add(a)
        if item.get("totalCalories") is not None:
            macros["cal"] = item["totalCalories"]
            macros["fat"] = item.get("totalFat", 0)
            macros["protein"] = item.get("totalProtein", 0)
            macros["carbs"] = item.get("totalCarbs", 0)

    return allergens, macros, default_ings


def get_item_price(item: dict) -> int:
    if item.get("sizes"):
        return item["sizes"][0]["price"]
    return item.get("basePrice", 0)


def get_medium_price(item: dict) -> int:
    sizes = item.get("sizes", [])
    if not sizes:
        return item.get("basePrice", 0)
    for s in sizes:
        label = s.get("label") or s.get("name", "")
        if label.lower() == "medium":
            return s["price"]
    return sizes[0]["price"]


def get_categories(menu_period: str = "all") -> list[dict]:
    categories = _MENU.get("categories", [])
    if menu_period == "all" or not _MENU.get("menuPeriods"):
        return categories
    period_data = _MENU.get("menuPeriods", {}).get(menu_period)
    if not period_data:
        return categories
    allowed_cat_ids = set(period_data.get("categories", []))
    return [c for c in categories if c["id"] in allowed_cat_ids]


def get_categories_list(menu_period: str = "all") -> list[dict]:
    categories = get_categories(menu_period)
    return [
        {
            "id": cat["id"],
            "name": cat["name"],
            "image": cat.get("image", ""),
            "item_count": len(cat.get("items", [])),
        }
        for cat in categories
    ]


def build_lightweight_item(item: dict) -> dict:
    return {
        "id": item["id"],
        "name": item["name"],
        "description": item.get("description", ""),
        "basePrice": item.get("basePrice", 0),
        "sizes": item.get("sizes", []),
        "tags": item.get("tags", []),
        "image": item.get("image", ""),
        "imageThumb": item.get("imageThumb", ""),
        "available": is_available(item["id"]),
    }


def search_items(
    keyword: str = "",
    category: str = "",
    dietary_tag: str = "",
    exclude_allergens: str = "",
    max_calories: int = 0,
    min_protein: int = 0,
    max_price: int = 0,
) -> list[dict]:
    results = []
    exclude_set = set()
    if exclude_allergens:
        exclude_set = {a.strip().lower() for a in exclude_allergens.split(",")}

    diet_rule = DIETARY_EXCLUSIONS.get(dietary_tag.lower()) if dietary_tag else None

    for cat in _MENU.get("categories", []):
        if category and cat["name"].lower() != category.lower():
            continue
        for item in cat.get("items", []):
            allergens, macros, default_ings = resolve_default_ingredients(item)
            price = get_item_price(item)

            if keyword:
                kw = keyword.lower()
                if kw not in item["name"].lower() and kw not in item.get("description", "").lower():
                    continue

            if exclude_set and exclude_set & {a.lower() for a in allergens}:
                continue

            if diet_rule:
                diet_allergen_exclude = diet_rule.get("allergens", set())
                if diet_allergen_exclude & {a.lower() for a in allergens}:
                    continue
                diet_ing_exclude = diet_rule.get("ingredient_ids", set())
                if diet_ing_exclude:
                    if default_ings:
                        item_ing_ids = {ing.get("id", "") for ing in default_ings}
                        if diet_ing_exclude & item_ing_ids:
                            continue
                    else:
                        item_diet_tags = {t.lower() for t in item.get("dietaryTags", [])}
                        if dietary_tag.lower() not in item_diet_tags and "vegan" not in item_diet_tags:
                            continue

            if max_calories and macros["cal"] > max_calories:
                continue
            if min_protein and macros["protein"] < min_protein:
                continue
            if max_price and price > max_price:
                continue

            results.append({
                "id": item["id"],
                "name": item["name"],
                "description": item.get("description", ""),
                "price": price,
                "calories": macros["cal"],
                "protein": macros["protein"],
                "allergens": sorted(allergens),
                "tags": item.get("tags", []),
                "image": item.get("image", ""),
                "available": is_available(item["id"]),
            })
    return results


def build_item_detail(item: dict) -> dict:
    allergens, macros, default_ings = resolve_default_ingredients(item)

    default_ingredients = []
    for ing in default_ings:
        entry: dict = {"name": ing["name"], "removable": ing["type"] != "fixed"}
        if ing["type"] == "levels":
            entry["levels"] = True
        default_ingredients.append(entry)

    available_additions = []
    for ing in item.get("ingredients", []):
        if ing.get("default", False):
            continue
        available_additions.append({"name": ing["name"], "price": ing.get("price", 0)})

    detail = {
        "id": item["id"],
        "name": item["name"],
        "description": item.get("description", ""),
        "basePrice": item.get("basePrice", 0),
        "sizes": item.get("sizes", []),
        "available": is_available(item["id"]),
        "tags": item.get("tags", []),
        "image": item.get("image", ""),
        "imageFull": item.get("imageFull", ""),
        "allergens": sorted(allergens),
        "macros": {
            "calories": macros["cal"],
            "fat": macros["fat"],
            "protein": macros["protein"],
            "carbs": macros["carbs"],
        },
        "default_ingredients": default_ingredients,
        "available_additions": available_additions,
        "choices": item.get("choices", []),
        "is_combo": item.get("isCombo", False),
        "combo_items": [],
    }

    if item.get("isCombo"):
        combo_items = []
        for ci in item.get("comboItems", []):
            combo_items.append({
                "item_id": ci["itemId"],
                "label": ci["label"],
            })
        detail["combo_items"] = combo_items

        individual_total = 0
        for ci in item.get("comboItems", []):
            ref = get_item_by_id(ci["itemId"])
            if ref:
                individual_total += get_medium_price(ref)
        detail["savings_vs_individual"] = individual_total - item.get("basePrice", 0)

    return detail


def find_matching_combos(item_ids: list[str]) -> list[dict]:
    item_id_set = set(item_ids)
    combos = []
    for cat in _MENU.get("categories", []):
        for item in cat.get("items", []):
            if not item.get("isCombo"):
                continue
            combo_item_ids = {ci["itemId"] for ci in item.get("comboItems", [])}
            if combo_item_ids.issubset(item_id_set):
                individual_total = 0
                for ci in item.get("comboItems", []):
                    ref = get_item_by_id(ci["itemId"])
                    if ref:
                        individual_total += get_medium_price(ref)
                savings = individual_total - item.get("basePrice", 0)
                if savings > 0:
                    combos.append({
                        "combo_id": item["id"],
                        "combo_name": item["name"],
                        "combo_price": item["basePrice"],
                        "individual_total": individual_total,
                        "savings": savings,
                        "matched_items": sorted(combo_item_ids),
                    })
    return combos
