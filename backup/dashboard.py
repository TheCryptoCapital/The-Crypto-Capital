import streamlit as st
import pandas as pd
import os

LOG_FILE = "trade_log.csv"

st.set_page_config(page_title="Trading Bot Dashboard", layout="wide")
st.title("📊 Reflections Bot - Live Trade Dashboard")

if os.path.exists(LOG_FILE):
    df = pd.read_csv(LOG_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    st.subheader("Trade Log")
    st.dataframe(df, height=400, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Trades", len(df))
    c2.metric("Unique Symbols", df["symbol"].nunique())
    net = df["profit"].sum() if "profit" in df.columns else 0
    c3.metric("Net PnL", f"${net:.2f}")

    st.subheader("📈 Cumulative PnL Over Time")
    pnl = (
        df
        .groupby(pd.Grouper(key="timestamp", freq="1min"))["profit"]
        .sum()
        .cumsum()
    )
    st.line_chart(pnl)

else:
    st.warning("No trades yet. Let your bot run first.")

