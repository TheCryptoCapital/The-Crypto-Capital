# main.py
import time
import logging
from trade_executor import execute_trade
from config import ACCOUNT_BALANCE, DAILY_PROFIT_TARGET, DAILY_MAX_LOSS
from performance_log import log_trade
from alerts_local import send_telegram_message  # logs to alerts.log

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

TRADING_SYMBOLS = [
    {"symbol": "XRPUSDT", "side": "Buy", "entry": 100, "tp": 105.0, "sl": 98.0},
    {"symbol": "SOLUSDT", "side": "Buy", "entry": 100, "tp": 105.0, "sl": 98.0},
    {"symbol": "ETHUSDT", "side": "Buy", "entry": 100, "tp": 105.0, "sl": 98.0},
    {"symbol": "ARBUSDT", "side": "Buy", "entry": 100, "tp": 105.0, "sl": 98.0},
    {"symbol": "BTCUSDT", "side": "Buy", "entry": 100, "tp": 105.0, "sl": 98.0},
]

POSITION_SIZE = 16.82  # test size for consistency

def main_loop():
    logging.info("Starting main loop...")

    for pair in TRADING_SYMBOLS:
        sym = pair["symbol"]
        side = pair["side"]
        entry = pair["entry"]
        tp = pair["tp"]
        sl = pair["sl"]

        try:
            logging.debug(f"Placing {side} {sym} @ {entry} (TP={tp}, SL={sl})")

            response = execute_trade(
                symbol=sym,
                side=side,
                entry=entry,
                quantity=POSITION_SIZE,
                take_profit=tp,
                stop_loss=sl
            )

            if response and isinstance(response, dict):
                if response.get("retCode") == 0:
                    send_telegram_message(f"[EXECUTED] {side} {POSITION_SIZE} {sym} at {entry} | TP: {tp}, SL: {sl}")
                    log_trade(
                        symbol=sym,
                        side=side,
                        quantity=POSITION_SIZE,
                        entry=entry,
                        take_profit=tp,
                        stop_loss=sl,
                        status="OPEN",
                        profit=None
                    )
                else:
                    logging.error(f"🔍 Full Bybit response: {response}")
                    logging.error(f"Trade failed for {sym}")
            else:
                logging.error(f"Unexpected response type: {response}")

        except Exception as e:
            logging.error(f"Error in {sym} loop: {e}")

        time.sleep(1)

if __name__ == "__main__":
    main_loop()

