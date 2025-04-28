from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import plotly.express as px
import uvicorn
import os
from pybit.unified_trading import HTTP
from dotenv import load_dotenv

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load API keys
load_dotenv()
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET")

session = HTTP(
    testnet=False,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    df = pd.read_csv("trades.csv") if os.path.exists("trades.csv") else pd.DataFrame()
    open_df = pd.read_csv("open_trades.csv") if os.path.exists("open_trades.csv") else pd.DataFrame()

    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df['day'] = df["timestamp"].dt.date

    daily_pnl = df.groupby("day")["pnl"].sum().cumsum().reset_index() if not df.empty else pd.DataFrame()
    symbol_pnl = df.groupby("symbol")["pnl"].sum().reset_index() if not df.empty else pd.DataFrame()

    total_closed_pnl = df["pnl"].sum() if not df.empty else 0.0

    # Calculate live Open PnL
    open_pnls = []
    if not open_df.empty:
        for index, row in open_df.iterrows():
            try:
                live_price = session.get_tickers(category="linear", symbol=row["symbol"])["result"]["list"][0]["lastPrice"]
                live_price = float(live_price)
                entry_price = float(row["take_profit"])  # Or change if needed
                qty = float(row["qty"])
                open_pnls.append((live_price - entry_price) * qty)
            except Exception as e:
                print(f"Error fetching price for {row['symbol']}: {e}")

    total_open_pnl = sum(open_pnls)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "daily_pnl": daily_pnl.to_dict(orient="list") if not daily_pnl.empty else [],
            "symbol_pnl": symbol_pnl.to_dict(orient="list") if not symbol_pnl.empty else [],
            "open_trades": open_df.to_dict(orient="records") if not open_df.empty else [],
            "recent_trades": df.to_dict(orient="records") if not df.empty else [],
            "total_open_pnl": round(total_open_pnl, 2),
            "total_closed_pnl": round(total_closed_pnl, 2),
            "open_pnls": open_pnls,  # pass full open pnl list
        },
    )

@app.get("/pnl-data")
async def get_pnl_data():
    if not os.path.exists("trades.csv"):
        return JSONResponse(content={"day": [], "pnl": []})

    df = pd.read_csv("trades.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df['day'] = df["timestamp"].dt.date

    daily_pnl = df.groupby("day")["pnl"].sum().cumsum().reset_index()
    return daily_pnl.to_dict(orient="list")

if __name__ == "__main__":
    uvicorn.run("dashboard_web:app", host="0.0.0.0", port=8000, reload=True)

