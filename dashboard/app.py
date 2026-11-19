import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Interactive Sales Dashboard")
st.caption("Explore sales, orders, products, and regions.")

data = pd.read_csv("dataset/sales_data.csv")
data["Order_Date"] = pd.to_datetime(data["Order_Date"])

st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Choose region",
    options=sorted(data["Region"].unique()),
    default=sorted(data["Region"].unique()),
)

categories = st.sidebar.multiselect(
    "Choose category",
    options=sorted(data["Category"].unique()),
    default=sorted(data["Category"].unique()),
)

filtered = data[
    data["Region"].isin(regions)
    & data["Category"].isin(categories)
]

if filtered.empty:
    st.warning("Select at least one region and one category.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered['Sales'].sum():,.0f}")
col2.metric("Total Orders", f"{filtered['Order_ID'].nunique():,}")
col3.metric("Total Profit", f"${filtered['Profit'].sum():,.0f}")

monthly = (
    filtered.assign(Month=filtered["Order_Date"].dt.to_period("M").astype(str))
    .groupby("Month", as_index=False)["Sales"]
    .sum()
)
product_sales = filtered.groupby("Product", as_index=False)["Sales"].sum()
region_sales = filtered.groupby("Region", as_index=False)["Sales"].sum()

left, right = st.columns(2)

with left:
    st.plotly_chart(
        px.line(monthly, x="Month", y="Sales", markers=True,
                title="Monthly Sales Trend"),
        use_container_width=True,
    )

with right:
    st.plotly_chart(
        px.bar(product_sales, x="Product", y="Sales",
               title="Sales by Product", color="Product"),
        use_container_width=True,
    )

st.plotly_chart(
    px.bar(region_sales, x="Region", y="Sales",
           title="Sales by Region", color="Region"),
    use_container_width=True,
)

st.subheader("Filtered Orders")
st.dataframe(filtered, use_container_width=True)
