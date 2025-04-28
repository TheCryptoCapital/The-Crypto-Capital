import requests

TELEGRAM_BOT_TOKEN = '7934261344:AAFWPngh0AuY5K9SWtxpwQ_XMwYlyGlSnKo'

TELEGRAM_CHAT_ID = '7346988127'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        r = requests.get(url, params=payload, timeout=5)
        print("✅ Telegram response:", r.json())
    except Exception as e:
        print("❌ Error sending message:", e)

send_telegram_message("🚀 Telegram is working, Jonathan! Bot is ready.")

