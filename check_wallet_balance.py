from pybit.unified_trading import HTTP
from config import BYBIT_API_KEY, BYBIT_API_SECRET

session = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET, testnet=False)

try:
    result = session.get_wallet_balance(accountType="UNIFIED")
    usdt_balance = result['result']['list'][0]['totalEquity']
    print(f"✅ Available USDT Balance: {usdt_balance}")
except Exception as e:
    print("❌ Error checking balance:", e)

