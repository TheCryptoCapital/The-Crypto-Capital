from pybit.unified_trading import HTTP
from config import BYBIT_API_KEY, BYBIT_API_SECRET
from telegram_alerts import send_telegram_message

session = HTTP(
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
    testnet=False
)

symbol = "DOGEUSDT"
side = "Buy"
order_type = "Market"
qty = "23960"  # ~ $500
time_in_force = "IOC"

try:
    response = session.place_order(
        category="linear",
        symbol=symbol,
        side=side,
        order_type=order_type,
        qty=qty,
        time_in_force=time_in_force,
        reduce_only=False
    )
    print("✅ Order placed:", response)
    send_telegram_message("✅ Live DOGE order placed.")
except Exception as e:
    print("❌ Error placing order:", e)
    send_telegram_message(f"❌ Order failed: {e}")

