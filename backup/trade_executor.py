# trade_executor.py

import logging
from config import BYBIT_API_KEY, BYBIT_API_SECRET

# ——— pick the right HTTP import & constructor ———
try:
    # pybit v5 “unified perpetual” client
    from pybit.unified_perpetual import HTTP

    session = HTTP(
        endpoint="https://api.bybit.com",    # supported here
        api_key=BYBIT_API_KEY,
        api_secret=BYBIT_API_SECRET
    )

except (ImportError, TypeError):
    try:
        # pybit v5 “unified trading” client (merged spot+perp)
        from pybit.unified_trading import HTTP

        session = HTTP(
            api_key=BYBIT_API_KEY,          # this constructor does NOT take `endpoint`
            api_secret=BYBIT_API_SECRET
        )

    except (ImportError, TypeError):
        # fallback for older pybit versions (spot)
        from pybit.spot import HTTP

        session = HTTP(
            endpoint="https://api.bybit.com",
            api_key=BYBIT_API_KEY,
            api_secret=BYBIT_API_SECRET
        )

def execute_trade(symbol: str, side: str, quantity: float,
                  entry_price: float, take_profit: float, stop_loss: float) -> bool:
    """
    Place a market order + TP/SL bracket. Returns True on success.
    """
    try:
        logging.debug(f"placing {side} market order for {quantity} {symbol}")
        # market order
        order_resp = session.place_active_order(
            symbol=symbol,
            side=side.upper(),
            order_type="Market",
            qty=quantity,
            time_in_force="ImmediateOrCancel",
            reduce_only=False,
            close_on_trigger=False
        )
        logging.debug(f"market order response: {order_resp}")

        # attach TP/SL
        tp_sl_resp = session.set_trading_stop(
            symbol=symbol,
            side=side.upper(),
            take_profit=take_profit,
            stop_loss=stop_loss,
            qty=quantity,
            time_in_force="PostOnly"
        )
        logging.debug(f"tp/sl response: {tp_sl_resp}")

        return True

    except Exception as e:
        logging.error(f"Trade execution error: {e}")
        return False

