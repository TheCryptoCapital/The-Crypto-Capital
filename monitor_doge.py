from pybit.unified_trading import HTTP
from config import BYBIT_API_KEY, BYBIT_API_SECRET

session = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET, testnet=False)

response = session.get_positions(category="linear", symbol="DOGEUSDT")
pos = response["result"]["list"][0]
print(f"\n📊 DOGEUSDT POSITION\nSize: {pos['size']}\nEntry: {pos.get('entryPrice', 'N/A')}\nUnrealized PnL: {pos['unrealisedPnl']}")



