from pybit.unified_trading import HTTP
from config import BYBIT_API_KEY, BYBIT_API_SECRET
import math

session = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET, testnet=False)

symbols = ["1000PEPEUSDT", "APTUSDT", "DOGEUSDT", "SOLUSDT"]

print("📊 Checking active positions...\n")

for symbol in symbols:
    try:
        result = session.get_positions(category="linear", symbol=symbol)
        position_data = result["result"]["list"][0]
        size = float(position_data.get("size", 0))
        entry_price = position_data.get("avgPrice", "")
        mark_price = position_data.get("markPrice", "")
        
        if size == 0 or entry_price == "" or mark_price == "":
            print(f"❌ {symbol} - No open position or missing data.\n")
            continue

        entry_price = float(entry_price)
        mark_price = float(mark_price)
        unrealized_pnl = round((mark_price - entry_price) * size, 4)

        print(f"✅ {symbol} Position")
        print(f"Size: {size}")
        print(f"Entry Price: {entry_price}")
        print(f"Current Price: {mark_price}")
        print(f"Unrealized PnL: {unrealized_pnl}\n")

    except Exception as e:
        print(f"⚠️ Error checking {symbol}:", e)

