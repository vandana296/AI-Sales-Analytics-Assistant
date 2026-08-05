import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_excel_data,
    find_main_dataset
)

from utils.executive import (
    calculate_kpis,
    category_performance,
    regional_performance,
    segment_performance,
    monthly_performance,
    top_products,
    loss_products,
    best_category,
    worst_category,
    best_region,
    worst_region
)

from utils.business_insights import (
    generate_business_summary,
    generate_executive_summary
)
from utils.pdf_report import generate_ai_report_pdf

from utils.chart_download import (
    dataframe_to_csv,
    figure_to_html,
    figure_to_png
)
from utils.theme import load_theme,show_header

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Insights",
    page_icon="📈",
    layout="wide"
)
load_theme()

show_header("📈 Executive Insights")

st.markdown(
    "Executive-level business insights powered by AI."
)

st.divider()

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

try:

    sheets = load_excel_data()

    sheet_name, df = find_main_dataset(sheets)

except Exception as e:

    st.error(e)
    st.stop()

# --------------------------------------------------
# KPIs
# --------------------------------------------------

kpis = calculate_kpis(df)

# --------------------------------------------------
# Prepare Data for AI Report
# --------------------------------------------------

category_df = category_performance(df)

region_df = regional_performance(df)

segment_df = segment_performance(df)

monthly_df = monthly_performance(df)

top_df = top_products(df)

loss_df = loss_products(df)

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Total Sales",
    f"£{kpis['Total Sales']:,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"£{kpis['Total Profit']:,.0f}"
)

col3.metric(
    "📦 Orders",
    f"{kpis['Total Orders']:,}"
)

col4.metric(
    "💹 Profit Margin",
    f"{kpis['Profit Margin']:.2f}%"
)

col5.metric(
    "🛒 Avg Order Value",
    f"£{kpis['Average Order Value']:,.0f}"
)

st.divider()

# --------------------------------------------------
# Business Summary
# --------------------------------------------------

st.subheader("📊 Business Summary")

st.markdown(
    generate_business_summary(df)
)

st.divider()

# --------------------------------------------------
# Best & Worst Performers
# --------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("🏆 Best Performers")

    category = best_category(df)

    region = best_region(df)

    st.success(f"""
### Best Category

**{category['Category']}**

💰 Sales: £{category['Sales']:,.0f}

📈 Profit: £{category['Profit']:,.0f}
""")

    st.success(f"""
### Best Region

**{region['Region']}**

💰 Sales: £{region['Sales']:,.0f}

📈 Profit: £{region['Profit']:,.0f}
""")

with right:

    st.subheader("⚠ Needs Attention")

    category = worst_category(df)

    region = worst_region(df)

    st.warning(f"""
### Worst Category

**{category['Category']}**

📉 Profit: £{category['Profit']:,.0f}
""")

    st.warning(f"""
### Worst Region

**{region['Region']}**

📉 Profit: £{region['Profit']:,.0f}
""")

st.divider()

# --------------------------------------------------
# Category Performance
# --------------------------------------------------

st.subheader("📊 Category Performance")

fig = px.bar(
    category_df,
    x="Category",
    y="Sales",
    color="Profit",
    text_auto=".2s",
    title="Sales by Category"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Regional Performance
# --------------------------------------------------

st.subheader("🌍 Regional Performance")

fig = px.bar(
    region_df,
    x="Region",
    y="Sales",
    color="Profit",
    text_auto=".2s",
    title="Sales by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
col1, col2, col3 = st.columns(3)

with col1:

    st.download_button(

        "📄 CSV",

        dataframe_to_csv(category_df),

        "category_sales.csv",

        "text/csv",

        use_container_width=True

    )

with col2:

    st.download_button(

        "🌐 HTML",

        figure_to_html(fig),

        "category_chart.html",

        "text/html",

        use_container_width=True

    )

with col3:

    st.download_button(

        "🖼 PNG",

        figure_to_png(fig),

        "category_chart.png",

        "image/png",

        use_container_width=True

    )

# --------------------------------------------------
# Monthly Trend
# --------------------------------------------------

st.subheader("📈 Monthly Sales Trend")

fig = px.line(
    monthly_df,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Products
# --------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("🏆 Top Products")

    st.dataframe(
        top_df,
        hide_index=True,
        use_container_width=True
    )

with right:

    st.subheader("📉 Loss Making Products")

    st.dataframe(
        loss_df,
        hide_index=True,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# AI Executive Report
# --------------------------------------------------

st.header("🤖 AI Executive Report")

st.info(
    "Generate a comprehensive AI-powered executive business report."
)

if "executive_report" not in st.session_state:
    st.session_state.executive_report = None


if st.button(
    "🚀 Generate AI Executive Report",
    use_container_width=True
):

    with st.spinner("Gemini AI is analyzing business performance..."):

        report = generate_executive_summary(

            kpis,

            category_df,

            region_df,

            segment_df,

            monthly_df,

            top_df,

            loss_df

        )

        st.session_state.executive_report = report

    st.success("Executive Report Generated Successfully!")


# --------------------------------------------------
# Display Report
# --------------------------------------------------

if st.session_state.executive_report:

    st.markdown(
        st.session_state.executive_report
    )

    pdf = generate_ai_report_pdf(

        title="AI Executive Business Report",

        report=st.session_state.executive_report,

        kpis={
            "Total Sales": f"£{kpis['Total Sales']:,.2f}",
            "Total Profit": f"£{kpis['Total Profit']:,.2f}",
            "Orders": kpis["Total Orders"],
            "Profit Margin": f"{kpis['Profit Margin']:.2f}%"
        }

    )

    st.download_button(

        label="📄 Download Executive Report (PDF)",

        data=pdf,

        file_name="Executive_Report.pdf",

        mime="application/pdf",

        use_container_width=True

    )