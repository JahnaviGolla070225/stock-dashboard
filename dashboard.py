import pandas as pd
import streamlit as st
import sqlite3
import plotly.express as px

# Streamlit App
st.title("📈 Real-Time Stock Dashboard")

# Connect to SQLite database
conn = sqlite3.connect("stock_data.db")

# Fetch actual stock data
query_actual = "SELECT timestamp AS date, close FROM stocks ORDER BY timestamp DESC LIMIT 100"
actual_df = pd.read_sql(query_actual, conn)

# Fetch forecast data
query_forecast = "SELECT ds AS date, yhat AS predicted_close FROM stock_forecast ORDER BY ds DESC LIMIT 50"
forecast_df = pd.read_sql(query_forecast, conn)

# Close database connection
conn.close()

# Convert 'date' to datetime format
actual_df['date'] = pd.to_datetime(actual_df['date'])
forecast_df['date'] = pd.to_datetime(forecast_df['date'])

# Merge actual and forecast data
actual_df['Type'] = "Actual"
forecast_df['Type'] = "Prediction"

# Rename columns to match
actual_df.rename(columns={'close': 'Stock Price'}, inplace=True)
forecast_df.rename(columns={'predicted_close': 'Stock Price'}, inplace=True)

# Combine both dataframes
combined_df = pd.concat([actual_df, forecast_df])

# Plot
fig = px.line(combined_df, x="date", y="Stock Price", color="Type",
              title="Actual vs Predicted Stock Prices",
              labels={"date": "Date", "Stock Price": "Price ($)"})

# Display chart
st.plotly_chart(fig)

# Show actual and forecast data in tables
st.write("### Latest Stock Prices")
st.dataframe(actual_df.head(10))

st.write("### Forecasted Stock Prices")
st.dataframe(forecast_df.head(10))
