LOYALTY_CUSTOMERS = {
    "555-0101": {
        "id": "loyalty-001",
        "name": "Amo",
        "phone": "555-0101",
        "points_balance": 2450,
        "usual_order": [
            {"item_name": "Double Smash Burger", "quantity": 1, "modifications": ["no onions"]},
            {"item_name": "Classic Fries", "quantity": 1, "size": "Large"},
            {"item_name": "Fountain Drink", "quantity": 1, "size": "Medium", "choices": ["Diet Coke"]},
        ],
    },
    "555-0102": {
        "id": "loyalty-002",
        "name": "Nika",
        "phone": "555-0102",
        "points_balance": 890,
        "usual_order": [
            {"item_name": "Bacon Cheese Combo", "quantity": 1},
            {"item_name": "Chicken Tenders", "quantity": 1, "size": "5 Piece", "choices": ["Buffalo"]},
        ],
    },
    "555-0103": {
        "id": "loyalty-003",
        "name": "Vato",
        "phone": "555-0103",
        "points_balance": 5200,
        "usual_order": [
            {"item_name": "Crispy Chicken Sandwich", "quantity": 1, "modifications": ["Nashville Hot"]},
            {"item_name": "Classic Fries", "quantity": 1, "size": "Medium"},
            {"item_name": "Fountain Drink", "quantity": 1, "size": "Large", "choices": ["Lemonade"]},
        ],
    },
    "555-0104": {
        "id": "loyalty-004",
        "name": "Levan",
        "phone": "555-0104",
        "points_balance": 1320,
        "usual_order": [
            {"item_name": "Breakfast Sandwich", "quantity": 1, "modifications": ["add bacon"]},
            {"item_name": "Hash Browns", "quantity": 1},
            {"item_name": "Coffee", "quantity": 1, "size": "Large", "choices": ["With Cream"]},
        ],
    },
    "555-0105": {
        "id": "loyalty-005",
        "name": "Mirian",
        "phone": "555-0105",
        "points_balance": 3100,
        "usual_order": [
            {"item_name": "Classic Combo", "quantity": 1},
            {"item_name": "Chocolate Brownie", "quantity": 1, "choices": ["A La Mode"]},
        ],
    },
    "555-0106": {
        "id": "loyalty-006",
        "name": "Beka",
        "phone": "555-0106",
        "points_balance": 670,
        "usual_order": [
            {"item_name": "Chicken Nuggets", "quantity": 1, "size": "20 Piece", "choices": ["Ranch"]},
            {"item_name": "Loaded Cheese Fries", "quantity": 1},
            {"item_name": "Fountain Drink", "quantity": 1, "size": "Large", "choices": ["Dr Pepper"]},
        ],
    },
    "555-0107": {
        "id": "loyalty-007",
        "name": "Giorgi",
        "phone": "555-0107",
        "points_balance": 4800,
        "usual_order": [
            {"item_name": "Grilled Chicken Sandwich", "quantity": 1},
            {"item_name": "Side Salad", "quantity": 1, "choices": ["Balsamic Vinaigrette"]},
            {"item_name": "Iced Tea", "quantity": 1, "size": "Large", "choices": ["Unsweet"]},
        ],
    },
    "555-0108": {
        "id": "loyalty-008",
        "name": "Megi",
        "phone": "555-0108",
        "points_balance": 1750,
        "usual_order": [
            {"item_name": "Veggie Burger", "quantity": 1},
            {"item_name": "Onion Rings", "quantity": 1, "size": "Medium"},
            {"item_name": "Milkshake", "quantity": 1, "size": "Regular", "choices": ["Strawberry"]},
        ],
    },
    "555-0109": {
        "id": "loyalty-009",
        "name": "Sandro",
        "phone": "555-0109",
        "points_balance": 2200,
        "usual_order": [
            {"item_name": "Double Smash Combo", "quantity": 1},
            {"item_name": "Onion Rings", "quantity": 1, "size": "Large"},
        ],
    },
    "555-0110": {
        "id": "loyalty-010",
        "name": "Levan",
        "phone": "555-0110",
        "points_balance": 980,
        "usual_order": [
            {"item_name": "Summer BBQ Burger", "quantity": 1},
            {"item_name": "Classic Fries", "quantity": 1, "size": "Large"},
            {"item_name": "Fountain Drink", "quantity": 1, "size": "Large", "choices": ["Coca-Cola"]},
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
    "loyalty-005": [
        {
            "order_id": "DT-1950",
            "date": "2026-07-13",
            "items": [
                {"name": "Classic Combo", "quantity": 1},
                {"name": "Chocolate Brownie", "quantity": 1, "choices": ["A La Mode"]},
            ],
            "total": 1728,
        },
    ],
    "loyalty-006": [
        {
            "order_id": "DT-1830",
            "date": "2026-07-10",
            "items": [
                {"name": "Chicken Nuggets", "quantity": 1, "size": "20 Piece", "choices": ["Ranch"]},
                {"name": "Loaded Cheese Fries", "quantity": 1},
                {"name": "Fountain Drink", "quantity": 1, "size": "Large", "choices": ["Dr Pepper"]},
            ],
            "total": 2397,
        },
    ],
    "loyalty-007": [
        {
            "order_id": "DT-1870",
            "date": "2026-07-11",
            "items": [
                {"name": "Grilled Chicken Sandwich", "quantity": 1},
                {"name": "Side Salad", "quantity": 1, "choices": ["Balsamic Vinaigrette"]},
                {"name": "Iced Tea", "quantity": 1, "size": "Large", "choices": ["Unsweet"]},
            ],
            "total": 1527,
        },
        {
            "order_id": "DT-1650",
            "date": "2026-07-04",
            "items": [
                {"name": "Tenders Combo", "quantity": 1},
                {"name": "Milkshake", "quantity": 1, "size": "Regular", "choices": ["Vanilla"]},
            ],
            "total": 1748,
        },
    ],
    "loyalty-008": [
        {
            "order_id": "DT-1910",
            "date": "2026-07-12",
            "items": [
                {"name": "Veggie Burger", "quantity": 1},
                {"name": "Onion Rings", "quantity": 1, "size": "Medium"},
                {"name": "Milkshake", "quantity": 1, "size": "Regular", "choices": ["Strawberry"]},
            ],
            "total": 1947,
        },
    ],
    "loyalty-009": [
        {
            "order_id": "DT-1880",
            "date": "2026-07-11",
            "items": [
                {"name": "Double Smash Combo", "quantity": 1},
                {"name": "Onion Rings", "quantity": 1, "size": "Large"},
            ],
            "total": 1998,
        },
        {
            "order_id": "DT-1700",
            "date": "2026-07-06",
            "items": [
                {"name": "Bacon Cheeseburger", "quantity": 1},
                {"name": "Classic Fries", "quantity": 1, "size": "Large"},
                {"name": "Fountain Drink", "quantity": 1, "size": "Medium", "choices": ["Coca-Cola"]},
            ],
            "total": 1547,
        },
    ],
    "loyalty-010": [
        {
            "order_id": "DT-1920",
            "date": "2026-07-13",
            "items": [
                {"name": "Summer BBQ Burger", "quantity": 1},
                {"name": "Classic Fries", "quantity": 1, "size": "Large"},
                {"name": "Fountain Drink", "quantity": 1, "size": "Large", "choices": ["Coca-Cola"]},
            ],
            "total": 2147,
        },
    ],
}

UNAVAILABLE_ITEMS = {
    "item-mac-and-cheese": "Mac & Cheese is temporarily unavailable. Try our Loaded Cheese Fries instead!",
    "item-milkshake": "Sorry, our ice cream machine is down right now. We've got Iced Tea and Fountain Drinks though!",
    "item-sundae": "Sorry, our ice cream machine is down right now. Try our Chocolate Brownie or Apple Pie instead!",
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
