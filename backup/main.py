import os
import time
import logging
import requests

from trade_executor import execute_trade
from risk_manager import calculate_position_size
from performance_log import log_trade

# === DEBUG SETUP ===
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)s:%(message)s')

# === TELEGRAM ALERTS SETUP ===
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise EnvironmentError(
        "Missing Telegram configuration: set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID as environment variables"
    )

def send_telegram_message(message: str):
    """
    Send a message to your configured Telegram chat.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        logging.info(f"Telegram status: {response.status_code}")
    except Exception as e:
        logging.error(f"Telegram error: {e}")

# === TRADE CONFIGS ===
trade_configs = [
    {"symbol": "XRPUSDT", "side": "Buy", "entry_price": 2.21, "take_profit": 2.90, "stop_loss": 2.10, "risk_usdt": 100},
    {"symbol": "SOLUSDT", "side": "Buy", "entry_price": 153.50, "take_profit": 162.00, "stop_loss": 149.00, "risk_usdt": 100},
    {"symbol": "ETHUSDT", "side": "Sell", "entry_price": 3198.00, "take_profit": 3120.00, "stop_loss": 3245.00, "risk_usdt": 100},
    {"symbol": "ARBUSDT", "side": "Buy", "entry_price": 1.65,  "take_profit": 1.80,  "stop_loss": 1.58,  "risk_usdt": 100},
    {"symbol": "BTCUSDT", "side": "Buy", "entry_price": 65300.00, "take_profit": 66200.00, "stop_loss": 64500.00, "risk_usdt": 100},
]


def main():
    """
    Main live trading loop: evaluates each config, executes trades, logs results, and sends alerts.
    """
    while True:
        for cfg in trade_configs:
            symbol     = cfg["symbol"]
            side       = cfg["side"]
            entry      = cfg["entry_price"]
            tp         = cfg["take_profit"]
            sl         = cfg["stop_loss"]
            risk       = cfg["risk_usdt"]

            logging.debug(f"Checking {symbol} {side}@{entry} (SL={sl}, TP={tp})")
            # 1) calculate how much to trade
            size = calculate_position_size(
                symbol=symbol,
                entry_price=entry,
                stop_loss=sl,
                risk_usdt=risk
            )
            logging.debug(f"Position size for {symbol}: {size}")

            # 2) place order via trade_executor
            resp = execute_trade(
                symbol=symbol,
                side=side,
                quantity=size,
                entry_price=entry,
                take_profit=tp,
                stop_loss=sl
            )
            logging.debug(f"execute_trade returned: {resp}")

            # 3) if order was placed, parse real fill price & compute PnL
            if resp:
                # Pull fill price from response
                if isinstance(resp, dict):
                    fill_price = float(
                        resp.get("avg_exec_price")
                        or resp.get("price")
                        or entry
                    )
                else:
                    fill_price = entry

                # Compute profit using real fill
                if side.lower() == "buy":
                    profit = (tp - fill_price) * size
                else:
                    profit = (fill_price - tp) * size

                # 4) log trade as FILLED
                log_trade(
                    symbol=symbol,
                    side=side,
                    quantity=size,
                    entry=fill_price,
                    tp=tp,
                    sl=sl,
                    status="FILLED",
                    profit=profit
                )

                # 5) send a Telegram alert
                send_telegram_message(
                    f"✅ Filled {side} {symbol} @ {fill_price:.4f}\n"
                    f"Size: {size}\n"
                    f"Take Profit: {tp}, Stop Loss: {sl}\n"
                    f"PnL: ${profit:.2f}"
                )
            else:
                logging.debug(f"No trade executed for {symbol}")

        # Wait before next cycle
        time.sleep(30)


if __name__ == "__main__":
    main()

