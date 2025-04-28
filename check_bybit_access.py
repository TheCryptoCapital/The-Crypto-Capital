import requests

try:
    r = requests.get("https://api.bybit.com/v5/market/tickers?category=linear")
    print("✅ SUCCESS — You can access Bybit.")
    print(r.json())
except Exception as e:
    print("❌ BLOCKED — Error accessing Bybit:")
    print(e)


