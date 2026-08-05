import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import (
    load_excel_data,
    find_main_dataset
)

from utils.theme import (
    load_theme,
    show_header
)
from utils.pdf_report import (
    generate_pdf_report,
    generate_ai_report_pdf
)
from utils.forecast_ai import generate_forecast_analysis

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Executive BI Dashboard",
    page_icon="📈",
    layout="wide"
)

load_theme()

show_header(
    "📈 Executive BI Dashboard",
    "Business Intelligence for Executive Decision Making"
)

# ==========================================================
# LOAD DATASET
# ==========================================================

try:

    sheets = load_excel_data()

    sheet_name, df = find_main_dataset(sheets)

except Exception as e:

    st.error(f"Unable to load dataset: {e}")

    st.stop()

# ==========================================================
# PREPARE DATA
# ==========================================================

df["Order Date"] = pd.to_datetime(df["Order Date"])

# ==========================================================
# EXECUTIVE KPIs
# ==========================================================

total_sales = df["Sales"].sum()

total_profit = df["Profit"].sum()

total_orders = len(df)

profit_margin = (
    total_profit / total_sales
) * 100

average_order_value = (
    total_sales / total_orders
)

st.subheader("📊 Executive KPI Dashboard")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "💰 Revenue",
    f"${total_sales:,.0f}"
)

k2.metric(
    "💵 Profit",
    f"${total_profit:,.0f}"
)

k3.metric(
    "📦 Orders",
    f"{total_orders:,}"
)

k4.metric(
    "📈 Margin",
    f"{profit_margin:.2f}%"
)

k5.metric(
    "🛒 Avg Order",
    f"${average_order_value:,.2f}"
)

st.divider()

# ==========================================================
# QUICK DATA SUMMARY
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("📋 Dataset Information")

    info = pd.DataFrame({

        "Metric": [

            "Rows",
            "Columns",
            "Categories",
            "Regions",
            "Segments"

        ],

        "Value": [

            len(df),

            len(df.columns),

            df["Category"].nunique(),

            df["Region"].nunique(),

            df["Segment"].nunique()

        ]

    })

    st.dataframe(
        info,
        hide_index=True,
        use_container_width=True
    )

with right:

    st.subheader("💡 Executive Highlights")

    best_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    best_category = (
        df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    st.success(f"""
### Business Snapshot

🏆 Best Region : **{best_region}**

🏆 Best Category : **{best_category}**

💰 Revenue : **${total_sales:,.0f}**

📈 Profit Margin : **{profit_margin:.2f}%**
""")

st.divider()
# ==========================================================
# MONTHLY REVENUE & PROFIT TREND
# ==========================================================

st.subheader("📈 Monthly Revenue & Profit Trend")

monthly = (
    df
    .groupby(
        df["Order Date"].dt.to_period("M")
    )
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

monthly["Month"] = monthly["Order Date"].astype(str)

fig = px.line(

    monthly,

    x="Month",

    y=["Revenue", "Profit"],

    markers=True,

    title="Monthly Revenue vs Profit"

)

fig.update_layout(
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# REVENUE VS PROFIT
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("💰 Revenue by Category")

    revenue_category = (

        df

        .groupby("Category")["Sales"]

        .sum()

        .reset_index()

        .sort_values(
            "Sales",
            ascending=False
        )

    )

    fig1 = px.bar(

        revenue_category,

        x="Category",

        y="Sales",

        color="Category",

        text_auto=".2f",

        title="Revenue by Category"

    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with right:

    st.subheader("💵 Profit by Category")

    profit_category = (

        df

        .groupby("Category")["Profit"]

        .sum()

        .reset_index()

        .sort_values(
            "Profit",
            ascending=False
        )

    )

    fig2 = px.bar(

        profit_category,

        x="Category",

        y="Profit",

        color="Category",

        text_auto=".2f",

        title="Profit by Category"

    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# ==========================================================
# CUMULATIVE REVENUE
# ==========================================================

st.subheader("📊 Cumulative Revenue Growth")

monthly["Cumulative Revenue"] = monthly["Revenue"].cumsum()

fig3 = px.area(

    monthly,

    x="Month",

    y="Cumulative Revenue",

    title="Cumulative Revenue Growth"

)

fig3.update_layout(
    height=450
)

st.plotly_chart(

    fig3,

    use_container_width=True

)

st.divider()
# ==========================================================
# REGIONAL PERFORMANCE
# ==========================================================

st.subheader("🌍 Regional Performance")

left, right = st.columns(2)

with left:

    region_sales = (
        df
        .groupby("Region")
        .agg(
            Revenue=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Revenue",
        color="Revenue",
        text_auto=".2f",
        title="Revenue by Region"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

with right:

    fig_region_profit = px.bar(
        region_sales,
        x="Region",
        y="Profit",
        color="Profit",
        text_auto=".2f",
        title="Profit by Region"
    )

    st.plotly_chart(
        fig_region_profit,
        use_container_width=True
    )

st.divider()

# ==========================================================
# CUSTOMER SEGMENT ANALYSIS
# ==========================================================

left, right = st.columns(2)

with left:

    segment_sales = (
        df
        .groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig_segment = px.pie(
        segment_sales,
        names="Segment",
        values="Sales",
        hole=0.45,
        title="Revenue by Customer Segment"
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )

with right:

    segment_profit = (
        df
        .groupby("Segment")["Profit"]
        .sum()
        .reset_index()
    )

    fig_segment_profit = px.bar(
        segment_profit,
        x="Segment",
        y="Profit",
        color="Segment",
        text_auto=".2f",
        title="Profit by Customer Segment"
    )

    st.plotly_chart(
        fig_segment_profit,
        use_container_width=True
    )

st.divider()

# ==========================================================
# TOP 10 PRODUCTS
# ==========================================================

st.subheader("🏆 Top 10 Products")

top_products = (
    df
    .groupby("Product Name")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
    .sort_values(
        "Revenue",
        ascending=False
    )
    .head(10)
)

fig_top = px.bar(
    top_products,
    x="Revenue",
    y="Product Name",
    orientation="h",
    color="Revenue",
    text_auto=".2f",
    title="Top 10 Revenue Generating Products"
)

fig_top.update_layout(
    height=500,
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(
    fig_top,
    use_container_width=True
)

st.divider()

# ==========================================================
# SUB-CATEGORY PERFORMANCE
# ==========================================================

st.subheader("📦 Top Sub-Categories")

subcategory = (
    df
    .groupby("Sub-Category")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
    .sort_values(
        "Revenue",
        ascending=False
    )
)

fig_sub = px.bar(
    subcategory,
    x="Sub-Category",
    y="Revenue",
    color="Profit",
    text_auto=".2f",
    title="Revenue by Sub-Category"
)

st.plotly_chart(
    fig_sub,
    use_container_width=True
)

st.divider()
# ==========================================================
# BUSINESS HEALTH SCORECARD
# ==========================================================

st.subheader("🏆 Business Health Scorecard")

avg_sales = df["Sales"].mean()
avg_profit = df["Profit"].mean()

sales_score = min((total_sales / 500000) * 100, 100)
profit_score = min((profit_margin / 20) * 100, 100)
order_score = min((total_orders / 1000) * 100, 100)

s1, s2, s3 = st.columns(3)

s1.metric(
    "📈 Revenue Score",
    f"{sales_score:.0f}/100"
)

s2.metric(
    "💵 Profit Score",
    f"{profit_score:.0f}/100"
)

s3.metric(
    "📦 Order Score",
    f"{order_score:.0f}/100"
)

st.divider()

# ==========================================================
# TOP PERFORMERS
# ==========================================================

st.subheader("🥇 Top Business Performers")

left, right = st.columns(2)

best_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

best_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .idxmax()
)

with left:

    st.success(f"""
### 🌍 Best Region

**{best_region}**

Highest Revenue Contributor
""")

with right:

    st.success(f"""
### 📦 Best Category

**{best_category}**

Highest Revenue Category
""")

st.divider()

# ==========================================================
# BUSINESS ALERTS
# ==========================================================

st.subheader("🚨 Executive Business Alerts")

if profit_margin >= 20:

    st.success(
        "🟢 Excellent profit margin."
    )

elif profit_margin >= 10:

    st.info(
        "🔵 Healthy business margin."
    )

else:

    st.warning(
        "🟠 Profit margin needs improvement."
    )

if total_sales > 1000000:

    st.success(
        "🚀 Revenue target exceeded."
    )

else:

    st.warning(
        "📊 Revenue target not yet achieved."
    )

if total_profit < 0:

    st.error(
        "❌ Business is operating at a loss."
    )

if total_orders < 500:

    st.warning(
        "📦 Order volume is relatively low."
    )

st.divider()

# ==========================================================
# REVENUE TARGET
# ==========================================================

st.subheader("🎯 Revenue Target Achievement")

target = 1000000

achievement = min(
    total_sales / target,
    1.0
)

st.progress(achievement)

st.metric(
    "Target Achievement",
    f"{achievement*100:.1f}%"
)

st.caption(
    f"Revenue Target: ${target:,.0f}"
)

st.divider()

# ==========================================================
# BUSINESS RANKING
# ==========================================================

st.subheader("🏅 Regional Ranking")

ranking = (
    df.groupby("Region")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values(
        "Revenue",
        ascending=False
    )
    .reset_index()
)

ranking.insert(
    0,
    "Rank",
    range(1, len(ranking)+1)
)

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)

st.divider()
# ==========================================================
# AI EXECUTIVE SUMMARY
# ==========================================================

st.subheader("🤖 AI Executive Summary")

try:

    executive_prompt = f"""
You are the CEO's Business Strategy Advisor.

Analyze the following business KPIs.

Revenue : ${total_sales:,.2f}

Profit : ${total_profit:,.2f}

Profit Margin : {profit_margin:.2f}%

Orders : {total_orders}

Best Region : {best_region}

Best Category : {best_category}

Generate:

1. Executive Summary

2. Business Performance

3. Risks

4. Opportunities

5. Strategic Recommendations

Keep the report concise and professional.
"""

    with st.spinner("Generating Executive Insights..."):

        executive_summary = generate_forecast_analysis(
            category=best_category,
            region=best_region,
            segment="All",
            quantity=total_orders,
            discount=0,
            prediction=total_sales
        )

    st.markdown(executive_summary)

except Exception as e:

    executive_summary = "AI Executive Summary unavailable."

    st.error(f"AI Error : {e}")

st.divider()

# ==========================================================
# AI BUSINESS RECOMMENDATIONS
# ==========================================================

st.subheader("💡 AI Business Recommendations")

left, right = st.columns(2)

with left:

    st.success(f"""
### 📈 Growth Opportunities

✅ Expand business in **{best_region}**

✅ Increase marketing for **{best_category}**

✅ Focus on high-value customers

✅ Improve customer retention

✅ Increase cross-selling
""")

with right:

    st.warning(f"""
### ⚠ Risk Monitoring

• Monitor discount levels

• Improve low-performing regions

• Review inventory planning

• Optimize operating costs

• Increase overall profitability
""")

st.divider()

# ==========================================================
# SWOT ANALYSIS
# ==========================================================

st.subheader("📊 Executive SWOT Analysis")

swot1, swot2 = st.columns(2)

with swot1:

    st.info("""
### 💪 Strengths

• Strong revenue performance

• Healthy product portfolio

• Diverse customer segments

• Regional presence
""")

    st.warning("""
### ⚠ Weaknesses

• Discount sensitivity

• Profit optimization needed

• Regional imbalance
""")

with swot2:

    st.success("""
### 🚀 Opportunities

• Market expansion

• Customer retention

• AI-driven forecasting

• Inventory optimization
""")

    st.error("""
### 🚨 Threats

• High discount pressure

• Competitive pricing

• Market uncertainty

• Seasonal demand changes
""")

st.divider()

# ==========================================================
# DOWNLOAD EXECUTIVE REPORT
# ==========================================================

st.subheader("📄 Executive Report")

executive_kpis = {

    "Revenue": f"${total_sales:,.2f}",
    "Profit": f"${total_profit:,.2f}",
    "Orders": total_orders,
    "Profit Margin": f"{profit_margin:.2f}%",
    "Best Region": best_region,
    "Best Category": best_category

}

pdf = generate_ai_report_pdf(

    title="Executive Business Intelligence Report",

    report=executive_summary,

    kpis=executive_kpis

)

st.download_button(

    "⬇ Download Executive Report",

    data=pdf,

    file_name="Executive_BI_Report.pdf",

    mime="application/pdf",

    use_container_width=True

)

st.divider()
# ==========================================================
# EXECUTIVE PERFORMANCE TIMELINE
# ==========================================================

st.subheader("📅 Executive Performance Timeline")

timeline = (
    df.groupby(df["Order Date"].dt.to_period("M"))
      .agg(
          Revenue=("Sales", "sum"),
          Profit=("Profit", "sum")
      )
      .reset_index()
)

timeline["Month"] = timeline["Order Date"].astype(str)

fig = px.area(
    timeline,
    x="Month",
    y="Revenue",
    title="Revenue Growth Timeline"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()
# ==========================================================
# BUSINESS HEALTH INDEX
# ==========================================================

st.subheader("🏥 Business Health Index")

health = (
    sales_score +
    profit_score +
    order_score
) / 3

if health >= 85:

    st.success(f"🟢 Business Health : {health:.0f}/100")

elif health >= 70:

    st.info(f"🔵 Business Health : {health:.0f}/100")

else:

    st.warning(f"🟠 Business Health : {health:.0f}/100")

st.progress(health / 100)

st.divider()
# ==========================================================
# QUICK FILTERS
# ==========================================================

st.subheader("🎛 Executive Filters")

selected_region = st.selectbox(
    "Filter Region",
    ["All"] + sorted(df["Region"].unique())
)

if selected_region != "All":

    filtered = df[
        df["Region"] == selected_region
    ]

else:

    filtered = df

st.write(
    f"Showing **{len(filtered)}** records."
)
# ==========================================================
# EXPORT DATA
# ==========================================================

st.subheader("📤 Export Executive Data")

csv = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(

    "⬇ Download CSV",

    csv,

    "Executive_Data.csv",

    "text/csv",

    use_container_width=True

)

st.divider()
# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "Developed by Vandana Singh | AI Sales Analytics Assistant | Machine Learning • Business Intelligence • Generative AI"
)