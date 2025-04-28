# utils.py
import os
import time
import hmac
import hashlib
from dotenv import load_dotenv

load_dotenv()

def sign_request(payload):
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")

    timestamp = str(int(time.time() * 1000))
    recv_window = "5000"

    sorted_data = dict(sorted(payload.items()))
    raw_query_string = "&".join(f"{key}={value}" for key, value in sorted_data.items())
    to_sign = f"{timestamp}{api_key}{recv_window}{raw_query_string}"

    signature = hmac.new(
        bytes(api_secret, "utf-8"),
        to_sign.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return {
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-SIGN": signature,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
        "Content-Type": "application/json"
    }

