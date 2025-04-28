import csv
import os
from datetime import datetime

def log_trade(symbol, side, qty, take_profit, stop_loss, order_id, result, pnl=None):
    file_exists = os.path.isfile('trades.csv')

    with open('trades.csv', mode='a', newline='') as file:
        writer = csv.writer(file)

        # If the file is new or empty, write the header first
        if not file_exists or os.stat('trades.csv').st_size == 0:
            writer.writerow(["timestamp", "symbol", "side", "qty", "take_profit", "stop_loss", "order_id", "result", "pnl"])

        # Write the trade data
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            side,
            qty,
            take_profit,
            stop_loss,
            order_id,
            result,
            pnl
        ])
