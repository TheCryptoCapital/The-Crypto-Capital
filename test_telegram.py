import os
from dotenv import load_dotenv
import requests

# Load .env variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MESSAGE = "✅ Telegram bot is working!"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": MESSAGE,
}

response = requests.post(url, data=payload)
print("Status Code:", response.status_code)
print("Response:", response.text)

