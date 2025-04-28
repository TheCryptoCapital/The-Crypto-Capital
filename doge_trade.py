import os
import math
import csv
import time
import pandas as pd
import ta
from datetime import datetime
from dotenv import load_dotenv
from pybit.unified_trading import HTTP
from trade_logger import log_trade

# Load API keys
load_dotenv()
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

# Create session
session = HTTP(
    testnet=False,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)

# --- Auto Risk Management ---

def check_max_daily_loss():
    if not os.path.exists('trades.csv'):
        return 0

    df = pd.read_csv('trades.csv')

    if df.empty:
        return 0

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    today = pd.Timestamp(datetime.now().date())

    today_trades = df[df["timestamp"].dt.date == today.date()]

    total_pnl_today = today_trades["pnl"].sum()

    if total_pnl_today <= -500:
        print(f"🛑 Max Daily Loss of $500 hit! Today's PnL: ${total_pnl_today}")
        print("⚠️ Stopping Bot to protect account.")
        exit()

    return total_pnl_today

# --- Trade Tracking Helpers ---

def log_open_trade(symbol, qty, take_profit, stop_loss, order_id):
    file_exists = os.path.isfile('open_trades.csv')
    with open('open_trades.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "symbol", "side", "qty", "take_profit", "stop_loss", "order_id", "result", "pnl"])
        writer.writerow([
            pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            "Buy",
            qty,
            take_profit,
            stop_loss,
            order_id,
            "OPEN",
            0.0
        ])

def handle_sell_trade(symbol, qty_to_sell, take_profit, stop_loss, order_id, pnl):
    if not os.path.exists('open_trades.csv'):
        print("❗ No open trades file found.")
        return

    df = pd.read_csv('open_trades.csv')

    matching = df[df["symbol"] == symbol]

    if matching.empty:
        print(f"❗ No open position found for {symbol}.")
        return

    idx = matching.index[0]
    open_qty = matching.loc[idx, "qty"]

    if qty_to_sell >= open_qty:
        log_closed_trade(symbol, open_qty, take_profit, stop_loss, order_id, pnl)
        df = df.drop(idx)
    else:
        df.at[idx, "qty"] = open_qty - qty_to_sell

    df.to_csv('open_trades.csv', index=False)

def log_closed_trade(symbol, qty, take_profit, stop_loss, order_id, pnl):
    file_exists = os.path.isfile('trades.csv')
    with open('trades.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "symbol", "side", "qty", "take_profit", "stop_loss", "order_id", "result", "pnl"])
        writer.writerow([
            pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            "Sell",
            qty,
            take_profit,
            stop_loss,
            order_id,
            "CLOSED",
            pnl
        ])

# --- SMART STRATEGY ---

symbols = ["DOGEUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT"]

while True:
    # ✅ Risk Management Check
    check_max_daily_loss()

    for symbol in symbols:
        try:
            klines = session.get_kline(
                category="linear",
                symbol=symbol,
                interval="15",
                limit=100
            )["result"]["list"]

            df = pd.DataFrame(klines)

            df = df.rename(columns={
                0: "timestamp",
                1: "open",
                2: "high",
                3: "low",
                4: "close",
                5: "volume",
                6: "turnover",
                7: "trade_count",
                8: "taker_buy_base",
                9: "taker_buy_quote",
                10: "ignore",
            })

            df["open"] = df["open"].astype(float)
            df["high"] = df["high"].astype(float)
            df["low"] = df["low"].astype(float)
            df["close"] = df["close"].astype(float)
            df["volume"] = df["volume"].astype(float)

            # Calculate Indicators
            df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
            df["ma_short"] = df["close"].rolling(window=10).mean()
            df["ma_long"] = df["close"].rolling(window=30).mean()
            macd = ta.trend.MACD(df["close"])
            df["macd"] = macd.macd()
            df["macd_signal"] = macd.macd_signal()
            df["adx"] = ta.trend.ADXIndicator(df["high"], df["low"], df["close"], window=14).adx()

            df["rsi"] = df["rsi"].astype(float)
            df["ma_short"] = df["ma_short"].astype(float)
            df["ma_long"] = df["ma_long"].astype(float)
            df["macd"] = df["macd"].astype(float)
            df["macd_signal"] = df["macd_signal"].astype(float)
            df["adx"] = df["adx"].astype(float)

            latest = df.iloc[-1]

            # --- Smart Entry ---
            if (latest["rsi"] < 30 and
                latest["ma_short"] > latest["ma_long"] and
                latest["macd"] > latest["macd_signal"] and
                latest["adx"] > 20):

                qty = 100  # adjust
                order = session.place_order(
                    category="linear",
                    symbol=symbol,
                    side="Buy",
                    order_type="Market",
                    qty=qty,
                    timeInForce="GoodTillCancel",
                    reduceOnly=False,
                )
                order_id = order['result']['orderId'] if order['retCode'] == 0 else 'N/A'
                log_open_trade(symbol, qty, take_profit=0, stop_loss=0, order_id=order_id)
                print(f"✅ SMART BUY {symbol} placed!")

            # --- Smart Exit ---
            elif (latest["rsi"] > 70 and
                  latest["ma_short"] < latest["ma_long"] and
                  latest["macd"] < latest["macd_signal"] and
                  latest["adx"] > 20):

                qty = 100
                order = session.place_order(
                    category="linear",
                    symbol=symbol,
                    side="Sell",
                    order_type="Market",
                    qty=qty,
                    timeInForce="GoodTillCancel",
                    reduceOnly=False,
                )
                order_id = order['result']['orderId'] if order['retCode'] == 0 else 'N/A'
                handle_sell_trade(symbol, qty, take_profit=0, stop_loss=0, order_id=order_id, pnl=0)
                print(f"✅ SMART SELL {symbol} placed!")

            else:
                print(f"🔍 {symbol}: No smart signal yet.")

        except Exception as e:
            print(f"⚠️ Error checking {symbol}: {e}")

    print("⏳ Waiting 60 seconds before checking again...")
    time.sleep(60)

