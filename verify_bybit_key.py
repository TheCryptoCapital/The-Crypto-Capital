from pybit.unified_trading import HTTP
from config import BYBIT_API_KEY, BYBIT_API_SECRET

# Connect to live Bybit
session = HTTP(
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
    testnet=False  # Change to True if using testnet keys
)

try:
    response = session.get_account_info()
    print("✅ API keys are working!")
    print(response)
except Exception as e:
    print("❌ Failed to authenticate. Please check your API keys.")
    print("Error:", e)
