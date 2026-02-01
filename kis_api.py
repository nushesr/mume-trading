import requests, os, time

BASE_URL = "https://openapi.koreainvestment.com:9443"

_token_cache = {
    "token": None,
    "expires": 0
}

_token_cache = {
    "token": None,
    "expires": 0
}

def place_order(ticker, price, qty):
    access_token = get_access_token()

    headers = {
        "authorization": f"Bearer {access_token}",
        "appkey": os.getenv("KIS_APP_KEY"),
        "appsecret": os.getenv("KIS_APP_SECRET"),
        "tr_id": "TTTC0802U"
    }

    body = {
        "CANO": os.getenv("KIS_ACCOUNT"),
        "ACNT_PRDT_CD": "01",
        "PDNO": ticker,
        "ORD_DVSN": "00",
        "ORD_QTY": str(qty),
        "ORD_UNPR": str(price)
    }

    r = requests.post(
        f"{BASE_URL}/uapi/domestic-stock/v1/trading/order-cash",
        headers=headers,
        json=body
    )
    return r.json()
