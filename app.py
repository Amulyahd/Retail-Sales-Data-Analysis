from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "retail_sales.csv"
DB = ROOT / "retail_sales.db"

st.set_page_config(page_title="Retail Sales Analysis", page_icon="📊", layout="wide")
st.title("📊 Retail Sales Data Analysis")
st.caption("Explore sales, products, countries and business performance using sample retail data.")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA, parse_dates=["OrderDate"])
    return df

df = load_data()

with sqlite3.connect(DB) as conn:
    df.to_sql("Sales", conn, if_exists="replace", index=False)

st.sidebar.header("Filters")
countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Country", countries)
products = ["All"] + sorted(df["Product"].dropna().unique().tolist())
selected_product = st.sidebar.selectbox("Product", products)
min_date, max_date = df["OrderDate"].min().date(), df["OrderDate"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)

filtered = df.copy()
if selected_country != "All":
    filtered = filtered[filtered["Country"] == selected_country]
if selected_product != "All":
    filtered = filtered[filtered["Product"] == selected_product]
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[(filtered["OrderDate"].dt.date >= date_range[0]) &
                        (filtered["OrderDate"].dt.date <= date_range[1])]

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

revenue = filtered["Sales"].sum()
orders = filtered["TransactionID"].nunique()
units = filtered["Quantity"].sum()
avg_order = revenue / orders if orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${revenue:,.2f}")
c2.metric("Transactions", f"{orders:,}")
c3.metric("Units Sold", f"{units:,}")
c4.metric("Average Order Value", f"${avg_order:,.2f}")

st.subheader("Revenue over time")
monthly = filtered.set_index("OrderDate").resample("MS")["Sales"].sum()
st.line_chart(monthly)

left, right = st.columns(2)
with left:
    st.subheader("Sales by product")
    by_product = filtered.groupby("Product")["Sales"].sum().sort_values(ascending=False)
    st.bar_chart(by_product)
with right:
    st.subheader("Sales by country")
    by_country = filtered.groupby("Country")["Sales"].sum().sort_values(ascending=False)
    st.bar_chart(by_country)

st.subheader("Top 10 transactions")
st.dataframe(filtered.sort_values("Sales", ascending=False).head(10), use_container_width=True)

st.subheader("Data preview")
st.dataframe(filtered, use_container_width=True)

csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data as CSV", csv_data, "filtered_retail_sales.csv", "text/csv")

st.info("This project uses an included sample dataset for learning and demonstration. Replace it with an appropriately licensed dataset for real analysis.")
