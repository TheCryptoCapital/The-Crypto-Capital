import os
from dotenv import load_dotenv

load_dotenv()

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

# TEMP TEST: Print keys to make sure they're loaded
print("KEY:", BYBIT_API_KEY)
print("SECRET:", BYBIT_API_SECRET)
