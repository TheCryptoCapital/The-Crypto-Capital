import smtplib
import os
from email.message import EmailMessage
from datetime import datetime
from config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

def send_trade_log_email():
    msg = EmailMessage()
    msg['Subject'] = f"Daily Trade Log Report - {datetime.utcnow().strftime('%Y-%m-%d')}"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content("Attached is today's trade log CSV.")

    try:
        with open("trade_log.csv", "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename="trade_log.csv")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("[EMAIL] Trade log sent successfully.")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

