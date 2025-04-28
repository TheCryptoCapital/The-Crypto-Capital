from pybit.unified_trading import HTTP
from config import BYBIT_API_KEY, BYBIT_API_SECRET

# Symbols your bot is monitoring
SYMBOLS = ["1000PEPEUSDT", "APTUSDT", "DOGEUSDT", "SOLUSDT"]

# Initialize session
session = HTTP(
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
    testnet=False
)

print("🔍 Checking open orders...\n")

for symbol in SYMBOLS:
    try:
        response = session.get_open_orders(category="linear", symbol=symbol)
        orders = response.get("result", {}).get("list", [])
        if orders:
            print(f"📌 {symbol} - {len(orders)} open order(s):")
            for order in orders:
                print(f"➡️ {order['side']} | {order['orderType']} | Qty: {order['qty']} | Price: {order['price']}")
        else:
            print(f"✅ {symbol} - No open orders.")
    except Exception as e:
        print(f"❌ Error checking {symbol}:", e)


