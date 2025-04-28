from pybit.unified_trading import HTTP
from config import BYBIT_API_KEY, BYBIT_API_SECRET
import time

session = HTTP(
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET
)

symbol = "DOGEUSDT"
qty = 100  # You can adjust this
side = "Buy"

# Place market order
order = session.place_order(
    category="linear",
    symbol=symbol,
    side=side,
    order_type="Market",
    qty=qty,
    time_in_force="GoodTillCancel"
)

print(f"✅ Forced market order placed: {order}")

