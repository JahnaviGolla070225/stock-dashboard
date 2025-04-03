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

# Fetch actual stock data from Supabase
response_actual = supabase.table("stocks").select("*").order("timestamp", desc=True).limit(100).execute()
stock_data = pd.DataFrame(response_actual.data)

# Check if the data has been successfully fetched
st.write("### Latest Stock Prices")
st.write(stock_data)

# Separate actual and forecast data based on non-null values in 'open', 'high', or 'low' columns
# Forecast data will have None in these columns
actual_stock_data = stock_data[stock_data['open'].notna() & stock_data['high'].notna() & stock_data['low'].notna()]
forecast_stock_data = stock_data[stock_data['open'].isna() | stock_data['high'].isna() | stock_data['low'].isna()]

# Line Chart for Stock Prices
fig, ax = plt.subplots(figsize=(10, 6))

# Plot Actual Data in Blue
ax.plot(pd.to_datetime(actual_stock_data['timestamp']), actual_stock_data['close'], label="Actual", color="blue")

# Plot Forecast Data in Red (Predictions) if any
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

# Rotate the x-axis labels to make them more readable
plt.xticks(rotation=45, ha='right')

# Adjust the figure size for better spacing
fig.tight_layout()

# Display the chart in Streamlit
st.pyplot(fig)
