import pandas as pd
import streamlit as st
from supabase import create_client
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Connect to Supabase
supabase_url = "https://rkeeqruvpphoadspsssy.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJrZWVxcnV2cHBob2Fkc3Bzc3N5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM2NjEzNTcsImV4cCI6MjA1OTIzNzM1N30.aXsli_TP0Wts2VYqaWZFP5S_tuoi6a_xZCaiCo1k0V0"
# Create Supabase client
supabase = create_client(supabase_url, supabase_key)

# Fetch stock data from Supabase
response = supabase.table("stocks").select("*").order("timestamp", desc=True).limit(100).execute()
stock_data = pd.DataFrame(response.data)

# Streamlit App Setup
st.title("📈 Real-Time Stock Dashboard")
st.write("### Latest Stock Prices")

# Show the raw stock data from Supabase
st.write("#### Raw Stock Data (from Supabase):")
st.dataframe(stock_data)

# Filter actual stock data (rows with valid 'open', 'high', 'low', 'close')
actual_stock_data = stock_data[
    stock_data['open'].notna() & stock_data['high'].notna() & stock_data['low'].notna() & stock_data['close'].notna()
]

# Filter forecasted stock data (rows where 'open', 'high', 'low' is NaN)
forecast_stock_data = stock_data[
    stock_data[['open', 'high', 'low']].isna().any(axis=1)
]

# Show the filtered actual and forecast data
st.write("#### Filtered Actual Stock Data:")
st.dataframe(actual_stock_data)

st.write("#### Filtered Forecast Stock Data:")
st.dataframe(forecast_stock_data)

# Line Chart for Stock Prices
fig, ax = plt.subplots(figsize=(10, 6))

# Plot Actual Data in Blue if available
if not actual_stock_data.empty:
    ax.plot(pd.to_datetime(actual_stock_data['timestamp']), actual_stock_data['close'], label="Actual", color="blue")

# Plot Forecast Data in Red if available
if not forecast_stock_data.empty:
    ax.plot(pd.to_datetime(forecast_stock_data['timestamp']), forecast_stock_data['close'], label="Forecast", color="red")

# Customize the plot
ax.set_title("Stock Price with Predictions")
ax.set_xlabel("Date")
ax.set_ylabel("Price (USD)")
ax.legend()

# Format x-axis for better readability
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Rotate the x-axis labels for better visibility
plt.xticks(rotation=45, ha='right')

# Adjust the figure size for better spacing
fig.tight_layout()

# Display the chart in Streamlit
st.pyplot(fig)
