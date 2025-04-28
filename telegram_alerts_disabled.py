# telegram_alerts.py
import requests, logging

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        resp = requests.post(url, json={"chat_id": chat_id, "text": message})
        logging.info(f"Telegram API status: {resp.status_code}")
    except Exception as e:
        logging.error(f"Telegram send error: {e}")

