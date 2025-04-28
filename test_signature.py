import time, hmac, hashlib, os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")
recv_window = "5000"
timestamp = str(int(time.time() * 1000))

params = {
    "symbol": "BTCUSDT",
    "side": "Buy",
    "orderType": "Market",
    "qty": "0.1",
    "category": "spot",
    "marketUnit": "baseCoin"
}

sorted_params = "".join(f"{k}{v}" for k, v in sorted(params.items()))
pre_sign = timestamp + api_key + recv_window + sorted_params
signature = hmac.new(api_secret.encode(), pre_sign.encode(), hashlib.sha256).hexdigest()

print("✅ Signature:", signature)

