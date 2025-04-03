import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect("stock_data.db")

# Load actual stock data
query_actual = "SELECT Datetime as Date, Close FROM stocks ORDER BY Datetime ASC"
actual_df = pd.read_sql(query_actual, conn)

# Load forecast data
query_forecast = "SELECT Date, Predicted_Close, Lower_Bound, Upper_Bound FROM stock_forecast ORDER BY Date ASC"
forecast_df = pd.read_sql(query_forecast, conn)

conn.close()

# Convert date columns to datetime
actual_df['Date'] = pd.to_datetime(actual_df['Date'])
forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])

# Streamlit Dashboard UI
st.title("📈 Stock Price Prediction Dashboard")

# Show actual stock prices
st.subheader("Historical Stock Prices")
st.line_chart(actual_df.set_index("Date")["Close"])

# Show forecast data
st.subheader("Stock Price Forecast")
fig, ax = plt.subplots()
ax.plot(forecast_df["Date"], forecast_df["Predicted_Close"], label="Predicted Price", color="blue")
ax.fill_between(forecast_df["Date"], forecast_df["Lower_Bound"], forecast_df["Upper_Bound"], color="blue", alpha=0.2)
ax.set_xlabel("Date")
ax.set_ylabel("Stock Price")
ax.legend()
st.pyplot(fig)
