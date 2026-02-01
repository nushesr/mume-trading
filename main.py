from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid, os

from kis_api import place_order

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

PENDING = {}

class PreviewReq(BaseModel):
    ticker: str
    seed: float
    avg_price: float
    current_price: float

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/order/preview")
def preview(req: PreviewReq):
    buy_price = min(req.avg_price * 1.05, req.current_price * 1.15)
    use_money = (req.seed / 40) / 2
    qty = int(use_money // buy_price)

    oid = str(uuid.uuid4())
    PENDING[oid] = {
        "ticker": req.ticker,
        "price": round(buy_price, 2),
        "qty": qty
    }

    return {"order_id": oid, **PENDING[oid]}

@app.post("/api/order/confirm/{order_id}")
def confirm(order_id: str):
    if order_id not in PENDING:
        return {"error": "invalid order"}

    order = PENDING.pop(order_id)

    # ⚠️ 실제로는 여기서 access_token 발급 후 사용
    result = place_order(
        order["ticker"],
        order["price"],
        order["qty"],
        access_token="ACCESS_TOKEN"
    )

    return {"status": "ORDER_SENT", "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
