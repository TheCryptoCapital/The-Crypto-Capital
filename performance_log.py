# performance_log.py
import logging

def log_trade(symbol, side, quantity, entry, tp, sl, status="OPEN", profit=None):
    logging.debug(f"Logged trade: {symbol} {side} at {entry} (SL {sl}, TP {tp})")
    # extend: write to CSV/db/etc.

