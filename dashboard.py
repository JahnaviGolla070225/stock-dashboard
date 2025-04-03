import pandas as pd
import streamlit as st
from supabase import create_client, Client

# Connect to Supabase
supabase_url = "https://rkeeqruvpphoadspsssy.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJrZWVxcnV2cHBob2Fkc3Bzc3N5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM2NjEzNTcsImV4cCI6MjA1OTIzNzM1N30.aXsli_TP0Wts2VYqaWZFP5S_tuoi6a_xZCaiCo1k0V0"
# Create Supabase client
supabase = create_client(supabase_url, supabase_key)

# Streamlit App Title
st.title("📈 Real-Time Stock Dashboard")

# Fetch Data from Supabase
try:
    response = supabase.table("stocks").select("*").order("timestamp", desc=True).limit(10).execute()
    if response.data:
        stock_data = pd.DataFrame(response.data)
        st.write("### Latest Stock Prices")
        st.dataframe(stock_data)
    else:
        st.warning("⚠️ No stock data found.")
except Exception as e:
    st.error(f"❌ Error fetching data: {e}")

# Line Chart for Stock Prices
if not stock_data.empty:
    st.write("### Stock Price Trend (Last 10 Entries)")
    st.line_chart(stock_data.set_index("timestamp")[["close"]])

# Refresh Button
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()
