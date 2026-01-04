import streamlit as st
import pandas as pd
import numpy as np

# --- Page Configuration ---
st.set_page_config(layout='wide', page_title="UrbanFix LA Dashboard")
st.title("UrbanSC Fix: Market Intelligence Dashboard")

# REMOVED: get_active_session() - Not needed for local CSV files

@st.cache_data
def obtain_data():
    # 1. Load the Integrated Data from the CSV you downloaded
    # Ensure this filename matches exactly what you upload to GitHub
    df_merged = pd.read_csv("contractor_data.csv")
    
    # 2. Convert date columns (CSV loads them as strings by default)
    # Using your existing column names from the Notebook/CSV export
    if 'PERMIT_DATE' in df_merged.columns:
        df_merged['PERMIT_DATE'] = pd.to_datetime(df_merged['PERMIT_DATE'], errors='coerce')
    
    # Ensure issue_year exists for your filters
    if 'ISSUE_YEAR' not in df_merged.columns and 'PERMIT_DATE' in df_merged.columns:
        df_merged['ISSUE_YEAR'] = df_merged['PERMIT_DATE'].dt.year

    return df_merged

# Load Data
df_main = obtain_data()

# --- Sidebar Filters ---
st.sidebar.header('Filters')

# 1. Year Slider Filter
if not df_main.empty:
    # Drop NaNs for the slider to prevent errors
    years = df_main['ISSUE_YEAR'].dropna().unique()
    date0 = int(min(years)) if len(years) > 0 else 2013
    date1 = int(max(years)) if len(years) > 0 else 2024
    min_year, max_year = st.sidebar.slider('Issue Year Range', date0, date1, value=(date0, date1))
else:
    min_year, max_year = 2013, 2024

# 2. Contractor Name Search
contractor_search = st.sidebar.text_input('Search Contractor Name:')

# Function to apply filters
@st.cache_data
def filter_data(df, min_y, max_y, search_term):
    # Filter by Year
    filtered = df[df['ISSUE_YEAR'].between(min_y, max_y)]
    
    # Filter by Name (if provided)
    if search_term:
        # Using 'BUSINESS_NAME' which is the column in your merged dataset
        filtered = filtered[filtered['BUSINESS_NAME'].astype(str).str.contains(search_term, case=False, na=False)]
        
    return filtered

# Apply the filters
df = filter_data(df_main, min_year, max_year, contractor_search)

# --- Main Metrics Section ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Total Permits', f"{len(df):,}")
with col2:
    st.metric('Total Valuation', f"${df['VALUATION'].sum()/1e6:.1f} M")
with col3:
    local_rate = df['IS_LOCAL'].mean() * 100 if len(df) > 0 else 0
    st.metric('Avg Local Project Rate', f"{local_rate:.2f}%")

st.divider()

# --- Charts Section ---
tab1, tab2, tab3 = st.tabs(["📍 Local Trends", "🏆 Market Share", "⚠️ Compliance Risk"])

with tab1:
    st.subheader("Contractor Localization Trends")
    local_trends = df.groupby('ISSUE_YEAR')['IS_LOCAL'].mean()
    st.line_chart(local_trends)
    st.caption("Y-axis: Share of projects done by local contractors")

with tab2:
    st.subheader("Top 10 Contractors by Valuation")
    total_val = df['VALUATION'].sum()
    if total_val > 0:
        top_builders = df.groupby("BUSINESS_NAME")["VALUATION"].sum().sort_values(ascending=False).head(10)
        top_pct = (top_builders / total_val) * 100
        st.bar_chart(top_pct)
        st.caption("Y-axis: Market Share (%)")
    else:
        st.info("No valuation data available.")

with tab3:
    st.subheader("Insurance Exempt Rates by Project Type")
    def get_category(desc):
        d = str(desc).lower()
        if "roof" in d: return "Roofing (High Risk)"
        if "pool" in d: return "Pool (High Risk)"
        if "hvac" in d: return "HVAC"
        if "solar" in d: return "Solar"
        return "Other"

    risk_df = df.copy()
    # Using 'AI_DESCRIPTION' from your export
    risk_df["Category"] = risk_df["AI_DESCRIPTION"].apply(get_category)
    plot_data = risk_df[risk_df["Category"] != "Other"]

    wc_col = "WORKERS_COMP_COVERAGE_TYPE"
    if wc_col in plot_data.columns and not plot_data.empty:
        exempt_rates = plot_data.groupby("Category")[wc_col].apply(lambda x: (x == "Exempt").mean() * 100)
        st.bar_chart(exempt_rates)
    else:
        st.info("No insurance data available.")

# --- Detailed Data Table ---
st.subheader('Detailed Data View')
st.dataframe(df.head(100), use_container_width=True)