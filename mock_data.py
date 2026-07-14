LOYALTY_CUSTOMERS = {
    "555-0101": {
        "id": "loyalty-001",
        "name": "Sarah",
        "phone": "555-0101",
        "points_balance": 2450,
        "available_rewards": [
            {"id": "reward-free-drink", "name": "Free Medium Drink", "description": "Any medium fountain drink"},
            {"id": "reward-2off-combo", "name": "$2 Off Any Combo", "description": "$2 discount on any combo meal"},
        ],
        "usual_order": [
            {"item_name": "Double Smash Burger", "quantity": 1, "modifications": ["no onions"]},
            {"item_name": "Classic Fries", "quantity": 1, "size": "Large"},
            {"item_name": "Fountain Drink", "quantity": 1, "size": "Medium", "choices": ["Diet Coke"]},
        ],
    },
    "555-0102": {
        "id": "loyalty-002",
        "name": "Marcus",
        "phone": "555-0102",
        "points_balance": 890,
        "available_rewards": [],
        "usual_order": [
            {"item_name": "Bacon Cheese Combo", "quantity": 1},
            {"item_name": "Chicken Tenders", "quantity": 1, "size": "5 Piece", "choices": ["Buffalo"]},
        ],
    },
    "555-0103": {
        "id": "loyalty-003",
        "name": "Emily",
        "phone": "555-0103",
        "points_balance": 5200,
        "available_rewards": [
            {"id": "reward-free-drink", "name": "Free Medium Drink", "description": "Any medium fountain drink"},
            {"id": "reward-free-cookie", "name": "Free Cookie", "description": "Any dessert item"},
            {"id": "reward-2off-combo", "name": "$2 Off Any Combo", "description": "$2 discount on any combo meal"},
        ],
        "usual_order": [
            {"item_name": "Crispy Chicken Sandwich", "quantity": 1, "modifications": ["Nashville Hot"]},
            {"item_name": "Classic Fries", "quantity": 1, "size": "Medium"},
            {"item_name": "Fountain Drink", "quantity": 1, "size": "Large", "choices": ["Lemonade"]},
        ],
    },
    "555-0104": {
        "id": "loyalty-004",
        "name": "James",
        "phone": "555-0104",
        "points_balance": 1320,
        "available_rewards": [
            {"id": "reward-free-drink", "name": "Free Medium Drink", "description": "Any medium fountain drink"},
        ],
        "usual_order": [
            {"item_name": "Breakfast Sandwich", "quantity": 1, "modifications": ["add bacon"]},
            {"item_name": "Hash Browns", "quantity": 1},
            {"item_name": "Coffee", "quantity": 1, "size": "Large", "choices": ["With Cream"]},
        ],
    },
}

LOYALTY_BY_ID = {v["id"]: v for v in LOYALTY_CUSTOMERS.values()}

ORDER_HISTORY = {
    "loyalty-001": [
        {
            "order_id": "DT-1847",
            "date": "2026-07-10",
            "items": [
                {"name": "Double Smash Burger", "quantity": 1, "modifications": ["no onions"]},
                {"name": "Classic Fries", "quantity": 1, "size": "Large"},
                {"name": "Fountain Drink", "quantity": 1, "size": "Medium", "choices": ["Diet Coke"]},
            ],
            "total": 1847,
        },
        {
            "order_id": "DT-1622",
            "date": "2026-07-03",
            "items": [
                {"name": "Double Smash Combo", "quantity": 1},
                {"name": "Chicken Nuggets", "quantity": 1, "size": "6 Piece", "choices": ["BBQ"]},
            ],
            "total": 2098,
        },
        {
            "order_id": "DT-1401",
            "date": "2026-06-26",
            "items": [
                {"name": "Grilled Chicken Sandwich", "quantity": 1},
                {"name": "Side Salad", "quantity": 1, "choices": ["Balsamic Vinaigrette"]},
                {"name": "Iced Tea", "quantity": 1, "size": "Large", "choices": ["Unsweet"]},
            ],
            "total": 1527,
        },
    ],
    "loyalty-002": [
        {
            "order_id": "DT-1790",
            "date": "2026-07-09",
            "items": [
                {"name": "Bacon Cheese Combo", "quantity": 1},
                {"name": "Chicken Tenders", "quantity": 1, "size": "5 Piece", "choices": ["Buffalo"]},
            ],
            "total": 2198,
        },
        {
            "order_id": "DT-1555",
            "date": "2026-07-02",
            "items": [
                {"name": "Breakfast Burrito", "quantity": 1, "modifications": ["add bacon"]},
                {"name": "Hash Browns", "quantity": 1},
                {"name": "Coffee", "quantity": 1, "size": "Medium", "choices": ["Black"]},
            ],
            "total": 1167,
        },
    ],
    "loyalty-003": [
        {
            "order_id": "DT-1820",
            "date": "2026-07-11",
            "items": [
                {"name": "Crispy Chicken Sandwich", "quantity": 1, "modifications": ["Nashville Hot"]},
                {"name": "Classic Fries", "quantity": 1, "size": "Medium"},
                {"name": "Fountain Drink", "quantity": 1, "size": "Large", "choices": ["Lemonade"]},
            ],
            "total": 1547,
        },
        {
            "order_id": "DT-1603",
            "date": "2026-07-04",
            "items": [
                {"name": "Chicken Combo", "quantity": 1},
                {"name": "Chocolate Brownie", "quantity": 1, "choices": ["A La Mode"]},
            ],
            "total": 1877,
        },
        {
            "order_id": "DT-1388",
            "date": "2026-06-27",
            "items": [
                {"name": "Tenders Combo", "quantity": 1},
                {"name": "Milkshake", "quantity": 1, "size": "Regular", "choices": ["Strawberry"]},
            ],
            "total": 1748,
        },
    ],
    "loyalty-004": [
        {
            "order_id": "DT-1900",
            "date": "2026-07-12",
            "items": [
                {"name": "Breakfast Sandwich", "quantity": 1, "modifications": ["add bacon"]},
                {"name": "Hash Browns", "quantity": 1},
                {"name": "Coffee", "quantity": 1, "size": "Large", "choices": ["With Cream"]},
            ],
            "total": 1108,
        },
    ],
}

UNAVAILABLE_ITEMS = {
    "item-summer-bbq-burger": "We just sold the last Summer BBQ Burger. Sorry about that — it's been really popular!",
    "item-mac-and-cheese": "Mac & Cheese is temporarily unavailable. Try our Loaded Cheese Fries instead!",
}

PROMO_CODES = {
    "SAVE10": {"type": "percent", "value": 10, "description": "10% off your order"},
    "FREEFRIES": {"type": "free_item", "item_id": "item-classic-fries", "size": "Medium", "description": "Free medium fries"},
    "COMBO5": {"type": "flat", "value": 500, "description": "$5 off any combo meal", "requires_combo": True},
    "BREAKFAST20": {"type": "percent", "value": 20, "description": "20% off your breakfast order"},
}

REWARD_DISCOUNTS = {
    "reward-free-drink": 249,
    "reward-free-cookie": 249,
    "reward-2off-combo": 200,
}
