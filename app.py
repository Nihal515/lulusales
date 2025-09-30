import streamlit as st
import pandas as pd

# ----------------------
# Load dataset from Excel
# ----------------------
@st.cache_data
def load_data():
    return pd.read_excel("lulu_sales_dataset.xlsx")

df = load_data()

# ----------------------
# Streamlit App Layout
# ----------------------
st.set_page_config(page_title="Lulu UAE Sales Dashboard", layout="wide")
st.title("📊 Lulu UAE - Sales Dashboard")

st.markdown("Insights from **transactions, demographics, loyalty, and ad spend.**")

# ----------------------
# Sidebar Filters
# ----------------------
st.sidebar.header("Filter Data")

age_range = st.sidebar.slider(
    "Select Age Range", 
    int(df.CustomerAge.min()), 
    int(df.CustomerAge.max()), 
    (20, 50)
)

gender_filter = st.sidebar.multiselect(
    "Select Gender", 
    options=df.Gender.unique(), 
    default=list(df.Gender.unique())
)

location_filter = st.sidebar.multiselect(
    "Select Location", 
    options=df.Location.unique(), 
    default=list(df.Location.unique())
)

income_filter = st.sidebar.multiselect(
    "Select Income Level", 
    options=df.IncomeLevel.unique(), 
    default=list(df.IncomeLevel.unique())
)

loyalty_filter = st.sidebar.multiselect(
    "Loyalty Member", 
    options=df.LoyaltyMember.unique(), 
    default=list(df.LoyaltyMember.unique())
)

category_filter = st.sidebar.multiselect(
    "Product Category", 
    options=df.ProductCategory.unique(), 
    default=list(df.ProductCategory.unique())
)

# ----------------------
# Apply Filters
# ----------------------
filtered_df = df[
    (df.CustomerAge.between(age_range[0], age_range[1])) &
    (df.Gender.isin(gender_filter)) &
    (df.Location.isin(location_filter)) &
    (df.IncomeLevel.isin(income_filter)) &
    (df.LoyaltyMember.isin(loyalty_filter)) &
    (df.ProductCategory.isin(category_filter))
]

# ----------------------
# KPI Metrics
# ----------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"AED {filtered_df['SalesAmount'].sum():,.2f}")
col2.metric("Transactions", filtered_df['NumTransactions'].sum())
col3.metric("Avg Sales", f"AED {filtered_df['SalesAmount'].mean():,.2f}")
col4.metric("Avg Loyalty Points Redeemed", f"{filtered_df['LoyaltyPointsRedeemed'].mean():.1f}")

# ----------------------
# Charts
# ----------------------
st.subheader("Sales by Location")
st.bar_chart(filtered_df.groupby("Location")["SalesAmount"].sum())

st.subheader("Sales by Product Category")
st.bar_chart(filtered_df.groupby("ProductCategory")["SalesAmount"].sum())

st.subheader("Ad Spend vs Sales (Location Wise)")
ad_sales = filtered_df.groupby("Location")[["SalesAmount", "AdSpendLocationWise"]].sum()
st.bar_chart(ad_sales)

st.subheader("Loyalty Members vs Non-Members (Sales)")
loyalty_sales = filtered_df.groupby("LoyaltyMember")["SalesAmount"].sum()
st.bar_chart(loyalty_sales)

# ----------------------
# Data Preview
# ----------------------
with st.expander("View Filtered Dataset"):
    st.dataframe(filtered_df)

