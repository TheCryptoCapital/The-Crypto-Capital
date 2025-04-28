import os, csv
from datetime import datetime

LOG_FILE = "trade_log.csv"

def log_trade(symbol, side, quantity, entry, tp, sl, status, profit):
    """
    Appends one row to trade_log.csv with exactly these 9 columns.
    """
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "timestamp","symbol","side","quantity",
                "entry","take_profit","stop_loss","status","profit"
            ])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol, side, quantity,
            entry, tp, sl, status,
            round(profit, 2)
        ])

