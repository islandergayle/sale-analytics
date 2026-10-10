import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page config
st.set_page_config(page_title="11.11 Sales Analytics Dashboard", layout="wide")

st.title("📊 11.11 Sales Analytics Dashboard")

# Cache data loading from results/ folder
@st.cache_data
def load_data():
    key_metrics = pd.read_csv("results/key_metrics.csv")
    category_revenue = pd.read_csv("results/category_revenue.csv")
    region_summary = pd.read_csv("results/region_summary.csv")
    orders_per_hour = pd.read_csv("results/orders_per_hour.csv")
    cancellation_by_payment = pd.read_csv("results/cancellation_by_payment.csv")
    
    return key_metrics, category_revenue, region_summary, orders_per_hour, cancellation_by_payment

try:
    key_metrics, category_revenue, region_summary, orders_per_hour, cancellation_by_payment = load_data()
except Exception as e:
    st.error("Error loading data from 'results/' folder. Make sure your CSVs are inside results/ directory.")
    st.stop()

# 1. Executive Summary
st.header("Executive Summary")
if not key_metrics.empty:
    row = key_metrics.iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₱{row.get('total_revenue', 0):,.2f}")
    col2.metric("Total Orders", f"{int(row.get('total_orders', 0)):,}")
    col3.metric("Cancellation Rate", f"{row.get('cancellation_rate', 0)*100:.2f}%")
    col4.metric("Avg Order Value", f"₱{row.get('average_order_value', 0):,.2f}")

st.divider()

# 2. Charts Section
col_cat, col_hour = st.columns(2)

with col_cat:
    st.subheader("🛍️ Revenue by Category")
    if not category_revenue.empty:
        # Bar chart requirement
        st.bar_chart(data=category_revenue, x=category_revenue.columns[0], y=category_revenue.columns[1])

with col_hour:
    st.subheader("⏰ Orders Per Hour")
    if not orders_per_hour.empty:
        # Line chart requirement
        st.line_chart(data=orders_per_hour, x=orders_per_hour.columns[0], y=orders_per_hour.columns[1])

st.divider()

# 3. Interactive Region Filter Requirement
st.subheader("🌍 Regional Performance")
if not region_summary.empty:
    regions = ["All"] + list(region_summary[region_summary.columns[0]].unique())
    selected_region = st.selectbox("Select Region Filter:", regions)
    
    if selected_region != "All":
        filtered_region = region_summary[region_summary[region_summary.columns[0]] == selected_region]
        st.dataframe(filtered_region, use_container_width=True)
    else:
        st.dataframe(region_summary, use_container_width=True)

st.divider()

# 4. AI Briefing Section (Part F)
st.header("🤖 AI Executive Briefing")

if st.button("Generate briefing"):
    # Read Gemini API key from Streamlit Secrets
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    
    if not api_key:
        st.error("Gemini API key is missing from Secrets. Please add GEMINI_API_KEY to Streamlit App Settings -> Secrets.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Prepare summary prompt
            metrics_summary = f"""
            Total Revenue: ₱{key_metrics.iloc[0].get('total_revenue', 0):,.2f}
            Total Orders: {key_metrics.iloc[0].get('total_orders', 0)}
            Cancellation Rate: {key_metrics.iloc[0].get('cancellation_rate', 0)*100:.2f}%
            Average Order Value: ₱{key_metrics.iloc[0].get('average_order_value', 0):,.2f}
            """
            
            prompt = f"""
            You are an expert sales analyst. Based strictly on these summary metrics from our 11.11 sale:
            {metrics_summary}

            Provide a concise 5-sentence briefing for the store owner summarizing key performance outcomes, followed by exactly ONE actionable recommendation for next year's 11.11 sale. Do not invent numbers.
            """
            
            with st.spinner("Generating AI Briefing..."):
                response = model.generate_content(prompt)
                st.success("Briefing Generated!")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Failed to generate briefing: {str(e)}")
