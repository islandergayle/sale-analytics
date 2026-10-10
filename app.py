import streamlit as st
import pandas as pd
import google.generativeai as genai

# Set page configuration
st.set_page_config(page_title="11.11 Sales Analytics Dashboard", layout="wide")

st.title("📊 Sales Analytics Dashboard")
st.markdown("Comprehensive overview of your sales performance, customer behavior, and regional summaries.")

# Helper to read files safely from results/ or root
@st.cache_data
def load_data():
    def read_csv(file_name):
        try:
            return pd.read_csv(f"results/{file_name}")
        except FileNotFoundError:
            return pd.read_csv(file_name)

    key_metrics = read_csv("key_metrics.csv")
    category_revenue = read_csv("category_revenue.csv")
    region_summary = read_csv("region_summary.csv")
    orders_per_hour = read_csv("orders_per_hour.csv")
    cancellation_by_payment = read_csv("cancellation_by_payment.csv")
    
    return key_metrics, category_revenue, region_summary, orders_per_hour, cancellation_by_payment

key_metrics, category_revenue, region_summary, orders_per_hour, cancellation_by_payment = load_data()

# --- Section 1: Executive Summary ---
st.header("1. Executive Summary")
if not key_metrics.empty:
    row = key_metrics.iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₱{row.get('total_revenue', 0):,.2f}")
    col2.metric("Total Orders", f"{int(row.get('total_orders', 0)):,}")
    col3.metric("Cancellation Rate", f"{row.get('cancellation_rate', 0)*100:.2f}%")
    col4.metric("Avg Order Value", f"₱{row.get('average_order_value', 0):,.2f}")

st.divider()

# --- Section 2: Revenue by Category & Region Summary ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🛍️ Revenue by Category")
    if not category_revenue.empty:
        cat_col = category_revenue.columns[0]
        val_col = category_revenue.columns[1] if len(category_revenue.columns) > 1 else cat_col
        st.bar_chart(category_revenue.set_index(cat_col)[val_col])
        st.dataframe(category_revenue, use_container_width=True)

with col_right:
    st.subheader("🌍 Region Summary & Interactive Filter")
    if not region_summary.empty:
        reg_col = region_summary.columns[0]
        val_col = region_summary.columns[1] if len(region_summary.columns) > 1 else reg_col
        
        # Region Filter Requirement
        region_options = ["All Regions"] + list(region_summary[reg_col].dropna().unique())
        selected_region = st.selectbox("Filter View by Region:", region_options)
        
        if selected_region != "All Regions":
            filtered_df = region_summary[region_summary[reg_col] == selected_region]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.bar_chart(region_summary.set_index(reg_col)[val_col])
            st.dataframe(region_summary, use_container_width=True)

st.divider()

# --- Section 3: Orders Per Hour & Cancellation by Payment ---
col_time, col_pay = st.columns(2)

with col_time:
    st.subheader("⏰ Orders Per Hour")
    if not orders_per_hour.empty:
        st.line_chart(orders_per_hour.set_index(orders_per_hour.columns[0]))

with col_pay:
    st.subheader("💳 Cancellations by Payment Method")
    if not cancellation_by_payment.empty:
        st.dataframe(cancellation_by_payment, use_container_width=True)

st.divider()

# --- Section 4: Generative AI Briefing ---
st.header("🤖 AI Executive Briefing")

if st.button("Generate briefing"):
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    
    if not api_key:
        st.error("Gemini API key is missing! Please configure GEMINI_API_KEY in Streamlit Settings -> Secrets.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            row = key_metrics.iloc[0]
            summary_info = f"""
            Total Revenue: ₱{row.get('total_revenue', 0):,.2f}
            Total Orders: {int(row.get('total_orders', 0)):,}
            Cancellation Rate: {row.get('cancellation_rate', 0)*100:.2f}%
            Average Order Value: ₱{row.get('average_order_value', 0):,.2f}
            """
            
            prompt = f"""
            You are a senior sales analyst. Based strictly on these 11.11 sale key metrics:
            {summary_info}

            Provide a 5-sentence briefing for the store owner summarizing performance, and conclude with exactly ONE strategic recommendation for next year's 11.11 sale. Do not invent details or numbers.
            """
            
            with st.spinner("Generating briefing via Gemini AI..."):
                response = model.generate_content(prompt)
                st.success("Briefing Generated Successfully!")
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Failed to generate briefing: {str(e)}")
