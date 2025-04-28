import logging

# Set up local alert logger
alert_logger = logging.getLogger("alert_logger")
alert_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("alerts.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
alert_logger.addHandler(file_handler)

def send_telegram_message(message):  # name stays the same for compatibility
    print(message)
    alert_logger.info(message)

