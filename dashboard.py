import pandas as pd
import streamlit as st

# Load the trade log
df = pd.read_csv("trade_log.csv")
df = df[df["status"].isin(["OPEN", "CLOSED"])]

# Drop any rows where 'timestamp' or 'symbol' or 'quantity' is missing
df.dropna(subset=["timestamp", "symbol", "quantity"], inplace=True)

# Convert timestamp and profit columns
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["profit"] = pd.to_numeric(df["profit"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# Only include rows with valid timestamp, quantity > 0, and status is OPEN or CLOSED
df = df[
    (df["timestamp"].notna()) &
    (df["quantity"] > 0) &
    (df["status"].isin(["OPEN", "CLOSED"]))
]

# Title
st.title("Live Trade Dashboard")

# Show metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Trades", len(df))
col2.metric("Winning Trades", len(df[df["profit"] > 0]))
col3.metric("Net Profit", f"${df['profit'].sum():.2f}")

# Show table
st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

