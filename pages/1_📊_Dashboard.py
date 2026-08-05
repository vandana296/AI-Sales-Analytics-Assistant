import pandas as pd
import streamlit as st

from utils.logger import logger
import utils.visualization as viz

st.write(__file__)

from utils.data_loader import (
    load_excel_data,
    find_main_dataset
)

from utils.filter import apply_filters
from utils.data_summary import get_dataset_summary
from utils.pdf_report import generate_pdf_report
from utils.theme import load_theme, show_header


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)
load_theme()


show_header("📊 AI Business Intelligence Dashboard")
st.markdown(
    "Analyze your Superstore sales using interactive dashboards, "
    "business KPIs and AI-powered insights."
)

st.markdown("---")


# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

try:

    logger.info("Loading Superstore dataset...")

    sheets = load_excel_data()

    sheet_name, df = find_main_dataset(sheets)

    if df is None:

        st.error("❌ No valid sales dataset found.")
        logger.error("No valid dataset detected.")

        st.stop()

    logger.info(f"Loaded sheet: {sheet_name}")

except FileNotFoundError:

    st.error("❌ Superstore Dataset.xlsx not found inside data folder.")
    logger.exception("Dataset file not found.")

    st.stop()

except Exception as e:

    st.error(f"Unexpected Error: {e}")
    logger.exception(e)

    st.stop()


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("⚙ Dashboard Filters")

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df["Region"].dropna().unique().tolist())
)

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["Category"].dropna().unique().tolist())
)

segment = st.sidebar.selectbox(
    "Segment",
    ["All"] + sorted(df["Segment"].dropna().unique().tolist())
)

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Refresh Dashboard"):

    st.cache_data.clear()
    st.rerun()


# ---------------------------------------------------
# Apply Filters
# ---------------------------------------------------

filtered_df = apply_filters(
    df,
    region,
    category,
    segment
)


# ---------------------------------------------------
# KPI Calculations
# ---------------------------------------------------

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()

profit_margin = 0

if total_sales > 0:

    profit_margin = (total_profit / total_sales) * 100


# ---------------------------------------------------
# Dataset Summary
# ---------------------------------------------------

summary = get_dataset_summary(filtered_df)


# ---------------------------------------------------
# Generate PDF
# ---------------------------------------------------

pdf = generate_pdf_report(
    summary,
    total_sales,
    total_profit,
    total_orders,
    profit_margin
)


# ---------------------------------------------------
# KPI Section
# ---------------------------------------------------

st.subheader("📈 Business KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.2f}"
    )

with col2:

    st.metric(
        "📈 Total Profit",
        f"${total_profit:,.2f}"
    )

with col3:

    st.metric(
        "🛒 Orders",
        f"{total_orders:,}"
    )

with col4:

    st.metric(
        "📊 Profit Margin",
        f"{profit_margin:.2f}%"
    )

st.markdown("---")
# ---------------------------------------------------
# Business Dashboard
# ---------------------------------------------------

st.subheader("📊 Business Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        viz.monthly_sales(filtered_df),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        viz.sales_by_category(filtered_df),
        use_container_width=True
    )

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        viz.sales_by_region(filtered_df),
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        viz.profit_by_segment(filtered_df),
        use_container_width=True
    )

st.plotly_chart(
    viz.top_products(filtered_df),
    use_container_width=True
)

st.markdown("---")


# ---------------------------------------------------
# Dataset Information
# ---------------------------------------------------

st.subheader("ℹ Dataset Information")

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.metric(
        "Detected Sheet",
        sheet_name
    )

with info_col2:
    st.metric(
        "Rows",
        f"{len(filtered_df):,}"
    )

with info_col3:
    st.metric(
        "Columns",
        len(filtered_df.columns)
    )

st.markdown("---")


# ---------------------------------------------------
# Dataset Summary
# ---------------------------------------------------

st.subheader("📋 Dataset Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Rows",
        summary["Rows"]
    )

with c2:
    st.metric(
        "Columns",
        summary["Columns"]
    )

with c3:
    st.metric(
        "Missing Values",
        summary["Missing Values"]
    )

with c4:
    st.metric(
        "Duplicate Rows",
        summary["Duplicate Rows"]
    )

c5, c6, c7, c8 = st.columns(4)

with c5:
    st.metric(
        "Memory (MB)",
        summary["Memory Usage (MB)"]
    )

with c6:
    st.metric(
        "Numeric Columns",
        summary["Numerical Columns"]
    )

with c7:
    st.metric(
        "Categorical Columns",
        summary["Categorical Columns"]
    )

with c8:
    st.metric(
        "Date Columns",
        summary["Date Columns"]
    )

st.markdown("---")


# ---------------------------------------------------
# Dataset Preview
# ---------------------------------------------------

st.subheader("📄 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=450
)

st.markdown("---")


# ---------------------------------------------------
# Data Dictionary
# ---------------------------------------------------

with st.expander("📖 Data Dictionary", expanded=False):

    dictionary = pd.DataFrame({
        "Column Name": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str)
    })

    st.dataframe(
        dictionary,
        use_container_width=True
    )

st.markdown("---")
# ---------------------------------------------------
# Missing Values Report
# ---------------------------------------------------

with st.expander("❌ Missing Values Report", expanded=False):

    missing_df = (
        filtered_df.isnull()
        .sum()
        .reset_index()
    )

    missing_df.columns = [
        "Column",
        "Missing Values"
    ]

    st.dataframe(
        missing_df,
        use_container_width=True
    )

st.markdown("---")


# ---------------------------------------------------
# Statistical Summary
# ---------------------------------------------------

with st.expander("📊 Statistical Summary", expanded=False):

    st.dataframe(
    filtered_df.describe(include="all"),
    use_container_width=True
)

st.markdown("---")


# ---------------------------------------------------
# Download PDF Report
# ---------------------------------------------------

st.subheader("📄 Download Business Report")

st.download_button(
    label="📥 Download PDF Report",
    data=pdf,
    file_name="AI_Business_Report.pdf",
    mime="application/pdf"
)

st.markdown("---")


# ---------------------------------------------------
# Quick Insights
# ---------------------------------------------------

st.subheader("💡 Quick Business Insights")

best_region = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

best_category = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .idxmax()
)

best_segment = (
    filtered_df.groupby("Segment")["Profit"]
    .sum()
    .idxmax()
)

st.success(
    f"""
    ✅ Highest Sales Region: **{best_region}**

    📦 Best Selling Category: **{best_category}**

    💰 Most Profitable Segment: **{best_segment}**
    """
)

st.markdown("---")


# ---------------------------------------------------
# Footer
# ---------------------------------------------------

logger.info("Dashboard loaded successfully.")

st.caption(
    "🚀 AI Business Intelligence Copilot | "
    "Built with Streamlit • Pandas • Plotly • Scikit-learn • Gemini AI"
)   