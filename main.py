from fastapi import FastAPI
from pydantic import BaseModel
from kis_api import place_order
import uuid

app = FastAPI()

PENDING_ORDERS = {}

class OrderRequest(BaseModel):
    ticker: str
    seed: float
    avg_price: float
    current_price: float

@app.post("/api/order/preview")
def preview_order(req: OrderRequest):
    avg5 = req.avg_price * 1.05
    price15 = req.current_price * 1.15
    buy_price = min(avg5, price15)

    split40 = req.seed / 40
    use_money = split40 / 2
    qty = int(use_money // buy_price)

    order_id = str(uuid.uuid4())

    PENDING_ORDERS[order_id] = {
        "ticker": req.ticker,
        "price": round(buy_price, 2),
        "qty": qty
    }

    return {
        "order_id": order_id,
        "ticker": req.ticker,
        "price": round(buy_price, 2),
        "qty": qty
    }
    
@app.post("/api/order/confirm/{order_id}")
def confirm_order(order_id: str):
    if order_id not in PENDING_ORDERS:
        return {"error": "Invalid or expired order"}

    order = PENDING_ORDERS.pop(order_id)

    # ⚠️ 여기서만 실제 주문
    result = place_order(
        order["ticker"],
        order["price"],
        order["qty"],
        access_token="ACCESS_TOKEN"
    )

    return {
        "status": "ORDER_SENT",
        "result": result
    }
