import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

ACCOUNT_BALANCE = 1682  # update with your real balance
LEVERAGE = 5
CAPITAL = 1500

DAILY_PROFIT_TARGET = 1000
DAILY_MAX_LOSS = 500

