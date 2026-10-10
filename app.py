import streamlit as st
import pandas as pd

st.title("Sales Analytics Dashboard")

# Load one of your CSVs directly from GitHub raw URL or relative path
@st.cache_data
def load_data():
    df = pd.read_csv("key_metrics.csv")
    return df

df = load_data()
st.write("### Key Metrics", df)
