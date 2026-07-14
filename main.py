import random
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import menu_data
from mock_data import (
    LOYALTY_BY_ID,
    LOYALTY_CUSTOMERS,
    ORDER_HISTORY,
    PROMO_CODES,
    REWARD_DISCOUNTS,
    UNAVAILABLE_ITEMS,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    menu_data.load_menu()
    yield


app = FastAPI(
    title="Fast X Food API",
    description="Mock backend for the Fast X Food AI drive-through demo. Powers menu browsing, ordering, loyalty, and agent tools.",
    version="2.0.0",
    lifespan=lifespan,
)


# ---------- Health ----------

@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


# ---------- 1. GET /v1/menu ----------

@app.get("/v1/menu", tags=["menu"])
def get_menu(
    branch_id: str = Query("branch-001"),
    menu_period: str = Query("all"),
):
    categories = menu_data.get_categories(menu_period)
    result_categories = []
    for cat in categories:
        items = [menu_data.build_lightweight_item(item) for item in cat.get("items", [])]
        result_categories.append({"id": cat["id"], "name": cat["name"], "items": items})

    menu = menu_data.get_menu()
    return {
        "restaurant_name": menu.get("name", "Fast X Food"),
        "branch_id": branch_id or "branch-001",
        "menu_period": menu_period,
        "categories": result_categories,
    }


# ---------- 1b. GET /v1/menu/categories ----------

@app.get("/v1/menu/categories", tags=["menu"])
def get_menu_categories(
    menu_period: str = Query("all"),
):
    return {"categories": menu_data.get_categories_list(menu_period)}


# ---------- 2. GET /v1/menu/search ----------

@app.get("/v1/menu/search", tags=["menu"])
def search_menu(
    branch_id: str = Query(""),
    keyword: str = Query(""),
    category: str = Query(""),
    dietary_tag: str = Query(""),
    exclude_allergens: str = Query(""),
    max_calories: Optional[int] = Query(None),
    min_protein: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
):
    results = menu_data.search_items(
        keyword=keyword,
        category=category,
        dietary_tag=dietary_tag,
        exclude_allergens=exclude_allergens,
        max_calories=max_calories or 0,
        min_protein=min_protein or 0,
        max_price=max_price or 0,
    )
    return {
        "query": {
            "keyword": keyword,
            "category": category,
            "exclude_allergens": exclude_allergens,
        },
        "results": results,
        "result_count": len(results),
    }


# ---------- 3. GET /v1/menu/items/{item_id} ----------

@app.get("/v1/menu/items/{item_id}", tags=["menu"])
def get_item(item_id: str, branch_id: str = Query("")):
    item = menu_data.get_item_by_id(item_id)
    if not item:
        return JSONResponse(status_code=404, content={"error": "Item not found", "item_id": item_id})
    return menu_data.build_item_detail(item)


# ---------- 4. GET /v1/availability/{item_id} ----------

@app.get("/v1/availability/{item_id}", tags=["availability"])
def check_availability(item_id: str):
    if item_id in UNAVAILABLE_ITEMS:
        return {
            "item_id": item_id,
            "available": False,
            "reason": UNAVAILABLE_ITEMS[item_id],
        }
    return {"item_id": item_id, "available": True}


# ---------- 4b. GET /v1/promo/validate ----------

@app.get("/v1/promo/validate", tags=["promo"])
def validate_promo(code: str = Query(...)):
    promo = PROMO_CODES.get(code.upper())
    if not promo:
        return {"valid": False, "code": code}
    return {"valid": True, "code": code.upper(), "type": promo["type"], "description": promo["description"]}


# ---------- 5. POST /v1/combos/check ----------

class ComboCheckRequest(BaseModel):
    item_ids: list[str]
    branch_id: str = "branch-001"


@app.post("/v1/combos/check", tags=["combos"])
def check_combos(req: ComboCheckRequest):
    combos = menu_data.find_matching_combos(req.item_ids)
    return {"combo_available": len(combos) > 0, "combos": combos}


# ---------- 6. GET /v1/loyalty/lookup ----------

@app.get("/v1/loyalty/lookup", tags=["loyalty"])
def loyalty_lookup(
    identifier: str = Query(...),
    type: str = Query("phone"),
):
    customer = None
    if type == "phone":
        customer = LOYALTY_CUSTOMERS.get(identifier)
    elif type in ("loyalty_id", "qr"):
        customer = LOYALTY_BY_ID.get(identifier)

    if not customer:
        return {"found": False, "message": "No loyalty account found."}

    return {"found": True, **customer}


# ---------- 7. GET /v1/loyalty/{customer_id}/orders ----------

@app.get("/v1/loyalty/{customer_id}/orders", tags=["loyalty"])
def loyalty_orders(customer_id: str, limit: int = Query(5)):
    if customer_id not in LOYALTY_BY_ID:
        return JSONResponse(status_code=404, content={"error": "Customer not found", "customer_id": customer_id})
    orders = ORDER_HISTORY.get(customer_id, [])[:limit]
    return {"customer_id": customer_id, "orders": orders}


# ---------- 8. POST /v1/loyalty/{customer_id}/redeem ----------

class RedeemRequest(BaseModel):
    reward_id: str
    order_subtotal: int


@app.post("/v1/loyalty/{customer_id}/redeem", tags=["loyalty"])
def redeem_reward(customer_id: str, req: RedeemRequest):
    customer = LOYALTY_BY_ID.get(customer_id)
    if not customer:
        return JSONResponse(status_code=400, content={"applied": False, "message": "Customer not found."})

    reward_ids = {r["id"] for r in customer.get("available_rewards", [])}
    if req.reward_id not in reward_ids:
        return JSONResponse(status_code=400, content={"applied": False, "message": "Reward not found or not available."})

    discount = REWARD_DISCOUNTS.get(req.reward_id, 0)
    new_subtotal = max(0, req.order_subtotal - discount)

    reward_name = next(
        (r["name"] for r in customer["available_rewards"] if r["id"] == req.reward_id),
        req.reward_id,
    )

    return {
        "applied": True,
        "reward_name": reward_name,
        "discount_cents": discount,
        "new_subtotal": new_subtotal,
    }


# ---------- 9. POST /v1/orders/submit ----------

class OrderItem(BaseModel):
    id: str
    name: str
    quantity: int = 1
    size: str = ""
    modifications: list[str] = []
    choices: list[str] = []
    unit_price: int = 0
    total_price: int = 0
    calories: int = 0


class OrderSubmitRequest(BaseModel):
    branch_id: str = "branch-001"
    items: list[OrderItem]
    subtotal: int
    notes: list[str] = []
    promo_code: str = ""
    loyalty_customer_id: str | None = None


@app.post("/v1/orders/submit", tags=["orders"])
def submit_order(req: OrderSubmitRequest):
    promo_discount = 0
    subtotal = req.subtotal

    if req.promo_code:
        promo = PROMO_CODES.get(req.promo_code.upper())
        if not promo:
            return JSONResponse(status_code=400, content={"success": False, "error": "Invalid promo code", "promo_code": req.promo_code})

        if promo["type"] == "percent":
            promo_discount = subtotal * promo["value"] // 100
        elif promo["type"] == "flat":
            if promo.get("requires_combo"):
                has_combo = any(
                    menu_data.get_item_by_id(i.id) and menu_data.get_item_by_id(i.id).get("isCombo")
                    for i in req.items
                )
                if not has_combo:
                    return JSONResponse(status_code=400, content={"success": False, "error": "Promo requires a combo meal", "promo_code": req.promo_code})
            promo_discount = promo["value"]
        elif promo["type"] == "free_item":
            for item in req.items:
                if item.id == promo["item_id"]:
                    ref = menu_data.get_item_by_id(item.id)
                    if ref:
                        promo_discount = menu_data.get_medium_price(ref)
                    break

    subtotal_after_promo = max(0, subtotal - promo_discount)
    tax = round(subtotal_after_promo * 0.085)
    total = subtotal_after_promo + tax

    order_number = f"DT-{random.randint(1000, 9999)}"
    wait_minutes = random.randint(3, 8)

    loyalty_points = total // 100 if req.loyalty_customer_id else 0

    return {
        "success": True,
        "order_number": order_number,
        "subtotal": subtotal,
        "promo_discount": promo_discount,
        "tax": tax,
        "total_with_tax": total,
        "total_display": f"${total / 100:.2f}",
        "estimated_wait_minutes": wait_minutes,
        "loyalty_points_earned": loyalty_points,
        "notes": req.notes,
    }


# ---------- 10. GET /v1/kitchen/wait-time ----------

@app.get("/v1/kitchen/wait-time", tags=["kitchen"])
def kitchen_wait_time(branch_id: str = Query("")):
    return {
        "available": True,
        "estimated_minutes": random.randint(2, 10),
        "queue_depth": random.randint(1, 6),
    }


# ---------- 11. POST /v1/feedback ----------

class FeedbackRequest(BaseModel):
    branch_id: str = "branch-001"
    session_id: str = ""
    type: str = "general"
    text: str = ""


_feedback_counter = 0


@app.post("/v1/feedback", tags=["feedback"])
def submit_feedback(req: FeedbackRequest):
    global _feedback_counter
    _feedback_counter += 1
    feedback_id = f"fb-{_feedback_counter:03d}"
    print(f"[FEEDBACK {feedback_id}] type={req.type} session={req.session_id} text={req.text}")
    return {"logged": True, "feedback_id": feedback_id, "message": "Thank you for your feedback."}


# ---------- 12. POST /v1/escalation ----------

class EscalationRequest(BaseModel):
    session_id: str = ""
    branch_id: str = "branch-001"
    reason: str = ""
    summary: str = ""
    order_state: list = []
    order_subtotal: int = 0
    loyalty_customer: dict | None = None
    promo_code: str = ""


_escalation_counter = 0


@app.post("/v1/escalation", tags=["escalation"])
def submit_escalation(req: EscalationRequest):
    global _escalation_counter
    _escalation_counter += 1
    escalation_id = f"esc-{_escalation_counter:03d}"
    print(f"[ESCALATION {escalation_id}] reason={req.reason} summary={req.summary}")
    print(f"  Full payload: {req.model_dump_json()}")
    return {
        "acknowledged": True,
        "escalation_id": escalation_id,
        "message": "Escalation received. Routing to staff.",
    }
