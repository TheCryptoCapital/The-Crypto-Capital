from pybit.unified_trading import HTTP
from config import BYBIT_API_KEY, BYBIT_API_SECRET

session = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET, testnet=False)

symbols = ["1000PEPEUSDT", "APTUSDT", "DOGEUSDT", "SOLUSDT"]

print("📊 Fetching raw position data...\n")

for symbol in symbols:
    try:
        response = session.get_positions(category="linear", symbol=symbol)
        print(f"\n🔍 {symbol} position data:\n{response}\n")
    except Exception as e:
        print(f"⚠️ Error checking {symbol}:", e)

