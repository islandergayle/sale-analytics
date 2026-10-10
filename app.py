import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

st.title("📊 Sales Analytics Dashboard")
st.markdown("Comprehensive overview of your sales performance, customer behavior, and regional summaries.")

# Cache data loading for better performance
@st.cache_data
def load_data():
    key_metrics = pd.read_csv("key_metrics.csv")
    category_revenue = pd.read_csv("category_revenue.csv")
    region_summary = pd.read_csv("region_summary.csv")
    orders_per_hour = pd.read_csv("orders_per_hour.csv")
    cancellation_by_payment = pd.read_csv("cancellation_by_payment.csv")
    
    return key_metrics, category_revenue, region_summary, orders_per_hour, cancellation_by_payment

key_metrics, category_revenue, region_summary, orders_per_hour, cancellation_by_payment = load_data()

# --- Section 1: Key Metrics Cards ---
st.header("1. Executive Summary")
if not key_metrics.empty:
    row = key_metrics.iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Revenue", f"${row.get('total_revenue', 0):,.2f}")
    col2.metric("Total Orders", f"{int(row.get('total_orders', 0)):,}")
    col3.metric("Cancellation Rate", f"{row.get('cancellation_rate', 0)*100:.2f}%")
    col4.metric("Avg Order Value", f"${row.get('average_order_value', 0):,.2f}")

st.divider()

# --- Section 2: Category Revenue & Region Summary ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🛍️ Revenue by Category")
    if not category_revenue.empty:
        st.dataframe(category_revenue, use_container_width=True)
        # If there's a numeric column for revenue, show a bar chart
        if len(category_revenue.columns) >= 2:
            st.bar_chart(category_revenue.set_index(category_revenue.columns[0]))

with col_right:
    st.subheader("🌍 Region Summary")
    if not region_summary.empty:
        st.dataframe(region_summary, use_container_width=True)
        if len(region_summary.columns) >= 2:
            st.bar_chart(region_summary.set_index(region_summary.columns[0]))

st.divider()

# --- Section 3: Time & Payment Analysis ---
col_time, col_pay = st.columns(2)

with col_time:
    st.subheader("⏰ Orders Per Hour")
    if not orders_per_hour.empty:
        st.line_chart(orders_per_hour.set_index(orders_per_hour.columns[0]))

with col_pay:
    st.subheader("💳 Cancellations by Payment Method")
    if not cancellation_by_payment.empty:
        st.dataframe(cancellation_by_payment, use_container_width=True)
