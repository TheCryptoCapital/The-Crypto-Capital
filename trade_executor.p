# For Linear Perpetual (Futures)
from pybit.unified_trading import HTTP
# OR if you're working with Spot trading:
# from pybit.spot import HTTP

from config import BYBIT_API_KEY, BYBIT_API_SECRET
import logging

# Initialize session with API keys
session = HTTP(api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)

# Function to execute trades
def execute_trade(symbol, side, entry, quantity, take_profit, stop_loss):
    try:
        order = session.place_order(
            category="linear",  # Use 'linear' for perpetual futures
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(quantity),
            takeProfit=str(take_profit),
            stopLoss=str(stop_loss),
        )
        logging.debug(f"Order response: {order}")
        return order
    except Exception as e:
        logging.error(f"Trade execution error: {e}")
        return None

# Fetch the market price for a given symbol
def fetch_mark_price(symbol):
    try:
        # Use public_get to get market data
        response = session.public_get('v2/public/tickers', params={"symbol": symbol})
        mark_price = float(response['result'][0]['last_price'])
        return mark_price
    except Exception as e:
        logging.error(f"Error fetching mark price for {symbol}: {e}")
        return None

# Fetch the minimum quantity for a given symbol
def get_min_qty(symbol):
    try:
        response = session.query_symbol(symbol=symbol)  # Correct method for getting min_qty in pybit v5.x
        min_qty = float(response['result']['lot_size_filter']['min_trading_qty'])
        return min_qty
    except Exception as e:
        logging.error(f"Error fetching minimum quantity for {symbol}: {e}")
        return None

