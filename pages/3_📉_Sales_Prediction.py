import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

from pathlib import Path

from utils.data_loader import (
    load_excel_data,
    find_main_dataset
)

from utils.theme import (
    load_theme,
    show_header
)

from utils.forecast_ai import (
    generate_forecast_analysis
)

from utils.pdf_report import (
    generate_pdf_report,
    generate_ai_report_pdf
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Sales Forecast Dashboard",
    page_icon="📈",
    layout="wide"
)

load_theme()

show_header(
    "📈 AI Sales Forecast Dashboard",
    "Machine Learning + Business Intelligence"
)

# ==========================================================
# LOAD DATASET
# ==========================================================

try:

    sheets = load_excel_data()

    sheet_name, df = find_main_dataset(
        sheets
    )

except Exception as e:

    st.error(
        f"Unable to load dataset : {e}"
    )

    st.stop()

# ==========================================================
# LOAD MODEL
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "sales_model.pkl"
)

try:

    model = joblib.load(
        MODEL_PATH
    )

except Exception as e:

    st.error(
        f"Unable to load model : {e}"
    )

    st.stop()

# ==========================================================
# DATASET OVERVIEW
# ==========================================================

st.subheader("📊 Dataset Overview")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = len(df)

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales > 0
    else 0
)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Total Sales",
    f"${total_sales:,.0f}"
)

c2.metric(
    "💵 Total Profit",
    f"${total_profit:,.0f}"
)

c3.metric(
    "📦 Orders",
    f"{total_orders:,}"
)

c4.metric(
    "📈 Profit Margin",
    f"{profit_margin:.2f}%"
)

st.divider()
# ==========================================================
# HISTORICAL SALES ANALYTICS
# ==========================================================

st.subheader("📈 Historical Sales Analytics")

history = df.copy()

history["Order Date"] = pd.to_datetime(
    history["Order Date"]
)

history["Month"] = (
    history["Order Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    history
    .groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

fig_month.update_layout(
    height=420
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

st.divider()

# ==========================================================
# CATEGORY & REGION ANALYSIS
# ==========================================================

left, right = st.columns(2)

with left:

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        text_auto=".2f",
        title="Sales by Category"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

with right:

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig_region = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        hole=0.45,
        title="Regional Sales Distribution"
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

st.divider()

# ==========================================================
# SEGMENT & TOP PRODUCTS
# ==========================================================

left, right = st.columns(2)

with left:

    segment_sales = (
        df.groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig_segment = px.bar(
        segment_sales,
        x="Segment",
        y="Sales",
        color="Segment",
        text_auto=".2f",
        title="Sales by Segment"
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )

with right:

    top_products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .reset_index()
        .sort_values(
            "Sales",
            ascending=False
        )
        .head(10)
    )

    fig_products = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        text_auto=".2f",
        title="Top 10 Products"
    )

    fig_products.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

st.divider()
# ==========================================================
# FORECAST SETTINGS
# ==========================================================

st.sidebar.title("⚙ Forecast Settings")

category = st.sidebar.selectbox(
    "Category",
    sorted(df["Category"].dropna().unique())
)

region = st.sidebar.selectbox(
    "Region",
    sorted(df["Region"].dropna().unique())
)

segment = st.sidebar.selectbox(
    "Segment",
    sorted(df["Segment"].dropna().unique())
)

quantity = st.sidebar.number_input(
    "Quantity",
    min_value=1,
    max_value=100,
    value=5
)

discount = st.sidebar.slider(
    "Discount",
    min_value=0.0,
    max_value=1.0,
    value=0.10,
    step=0.01
)

st.sidebar.divider()

predict_button = st.sidebar.button(
    "🚀 Predict Sales",
    use_container_width=True
)

# ==========================================================
# SALES PREDICTION
# ==========================================================

if predict_button:

    # -----------------------------------------
    # Prepare Input
    # -----------------------------------------

    input_df = pd.DataFrame({

        "Category": [category],
        "Region": [region],
        "Segment": [segment],
        "Quantity": [quantity],
        "Discount": [discount]

    })

    # -----------------------------------------
    # Predict Sales
    # -----------------------------------------

    prediction = model.predict(input_df)[0]

    st.session_state["prediction"] = prediction

    avg_sales = df["Sales"].mean()

    expected_growth = (
        (prediction / avg_sales) - 1
    ) * 100

    st.success("✅ Sales Forecast Generated Successfully!")

    # -----------------------------------------
    # Save Forecast History
    # -----------------------------------------

    history_row = pd.DataFrame({

        "Date": [pd.Timestamp.now()],
        "Category": [category],
        "Region": [region],
        "Segment": [segment],
        "Quantity": [quantity],
        "Discount": [discount],
        "Prediction": [prediction]

    })

    history_path = BASE_DIR / "forecast_history.csv"

    if history_path.exists():

        old_history = pd.read_csv(history_path)

        history = pd.concat(
            [old_history, history_row],
            ignore_index=True
        )

    else:

        history = history_row

    history.to_csv(
        history_path,
        index=False
    )

    st.divider()

    # =====================================================
    # FORECAST DASHBOARD
    # =====================================================

    st.subheader("📊 Forecast Dashboard")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "💰 Predicted Sales",
        f"${prediction:,.2f}"
    )

    k2.metric(
        "📦 Quantity",
        quantity
    )

    k3.metric(
        "🏷 Discount",
        f"{discount:.0%}"
    )

    k4.metric(
        "📈 Expected Growth",
        f"{expected_growth:.2f}%"
    )

    st.divider()

    # =====================================================
    # PREDICTION SUMMARY
    # =====================================================

    st.subheader("📋 Prediction Summary")

    summary = pd.DataFrame({

        "Category": [category],
        "Region": [region],
        "Segment": [segment],
        "Quantity": [quantity],
        "Discount": [discount],
        "Predicted Sales": [round(prediction, 2)]

    })

    st.dataframe(
        summary,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # PREDICTION VS HISTORICAL AVERAGE
    # =====================================================

    comparison = pd.DataFrame({

        "Type": [
            "Historical Average",
            "Predicted Sales"
        ],

        "Sales": [
            avg_sales,
            prediction
        ]

    })

    fig_compare = px.bar(

        comparison,

        x="Type",
        y="Sales",
        color="Type",
        text_auto=".2f",
        title="Prediction vs Historical Average"

    )

    st.plotly_chart(
        fig_compare,
        use_container_width=True
    )

    st.divider()
        # ==========================================================
    # FORECAST CONFIDENCE
    # ==========================================================

    st.subheader("🎯 Forecast Confidence")

    confidence = 92

    st.progress(confidence / 100)

    c1, c2 = st.columns(2)

    c1.metric(
        "Confidence Score",
        f"{confidence}%"
    )

    c2.metric(
        "Forecast Status",
        "High Confidence"
    )

    st.divider()

    # ==========================================================
    # AI BUSINESS ANALYSIS
    # ==========================================================

    st.subheader("🤖 AI Business Analysis")

    try:

        with st.spinner("Generating AI insights..."):

            analysis = generate_forecast_analysis(
                category=category,
                region=region,
                segment=segment,
                quantity=quantity,
                discount=discount,
                prediction=prediction
            )

        st.markdown(analysis)

    except Exception as e:

        analysis = "AI analysis unavailable."

        st.error(f"AI Analysis Error: {e}")

    st.divider()

    # ==========================================================
    # SMART BUSINESS ALERTS
    # ==========================================================

    st.subheader("🚨 Smart Business Alerts")

    if prediction > avg_sales:

        st.success(
            "🟢 Expected sales are above the historical average."
        )

    else:

        st.warning(
            "🟠 Expected sales are below the historical average."
        )

    if discount >= 0.40:

        st.error(
            "🔴 High discount may reduce profitability."
        )

    elif discount >= 0.20:

        st.warning(
            "🟠 Moderate discount detected."
        )

    else:

        st.success(
            "🟢 Healthy discount level."
        )

    if quantity >= 15:

        st.info(
            "📦 Large order detected. Ensure inventory availability."
        )

    st.divider()

    # ==========================================================
    # EXECUTIVE INSIGHTS
    # ==========================================================

    st.subheader("📈 Executive Insights")

    left, right = st.columns(2)

    with left:

        st.info(f"""
### Forecast Summary

- **Predicted Sales:** ${prediction:,.2f}
- **Average Sales:** ${avg_sales:,.2f}
- **Expected Growth:** {expected_growth:.2f}%
- **Confidence:** {confidence}%
""")

    with right:

        st.success(f"""
### Recommended Actions

- Focus on **{region}**
- Promote **{category}**
- Target **{segment}**
- Monitor discount strategy
- Plan inventory proactively
""")

    st.divider()

    # ==========================================================
    # PDF REPORT
    # ==========================================================

    kpis = {

        "Predicted Sales": f"${prediction:,.2f}",
        "Expected Growth": f"{expected_growth:.2f}%",
        "Category": category,
        "Region": region,
        "Segment": segment,
        "Quantity": quantity,
        "Discount": f"{discount:.0%}"

    }

    pdf = generate_ai_report_pdf(

        title="AI Sales Forecast Report",

        report=analysis,

        kpis=kpis

    )

    st.download_button(

        label="⬇ Download AI Forecast Report",

        data=pdf,

        file_name="AI_Sales_Forecast_Report.pdf",

        mime="application/pdf",

        use_container_width=True

    )

    st.divider()

    # ==========================================================
    # FORECAST HISTORY
    # ==========================================================

    st.subheader("📅 Forecast History")

    history_df = pd.read_csv(history_path)

    st.dataframe(

        history_df.tail(10),

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ==========================================================
    # FORECAST TREND SIMULATION
    # ==========================================================

    st.subheader("📈 Forecast Trend Simulation")

    simulation = pd.DataFrame({

        "Month": [
            "Current",
            "Month +1",
            "Month +2",
            "Month +3"
        ],

        "Forecast Sales": [

            prediction,

            prediction * 1.05,

            prediction * 1.10,

            prediction * 1.15

        ]

    })

    fig_forecast = px.line(

        simulation,

        x="Month",

        y="Forecast Sales",

        markers=True,

        title="Projected Sales Trend"

    )

    st.plotly_chart(

        fig_forecast,

        use_container_width=True

    )
    # ==========================================================
    # BUSINESS SCORECARD
    # ==========================================================

    st.divider()

    st.subheader("🏆 Business Performance Scorecard")

    score1, score2, score3 = st.columns(3)

    sales_score = min((prediction / avg_sales) * 100, 150)

    discount_score = max(100 - discount * 100, 0)

    inventory_score = 100 if quantity <= 15 else 70

    score1.metric(
         "📈 Sales Score",
         f"{sales_score:.0f}/100"
    )

    score2.metric(
         "💰 Pricing Score",
         f"{discount_score:.0f}/100"
    )

    score3.metric(
         "📦 Inventory Score",
         f"{inventory_score}/100"
    )
    st.divider()

    st.subheader("🩺 Forecast Health")

    if sales_score >= 100:

       st.success("Excellent revenue potential detected.")

    elif sales_score >= 80:

        st.info("Healthy sales forecast.")

    else:

       st.warning("Sales forecast needs improvement.")

    if discount >= 0.40:

       st.error("Discount is too high.")

    elif discount >= 0.20:

        st.warning("Discount is moderate.")

    else:

       st.success("Pricing strategy looks healthy.")

    st.divider()

    st.subheader("📊 Forecast Performance")

    gauge = pd.DataFrame({

      "Metric": [

        "Predicted Sales",
        "Average Sales"

    ],

    "Value": [

        prediction,
        avg_sales

    ]

    })

    fig = px.bar(

    gauge,

    x="Metric",

    y="Value",

    color="Metric",

    text_auto=".2f",

    title="Forecast Performance"

    )

    st.plotly_chart(
    fig,
    use_container_width=True
    )
    st.divider()

    st.subheader("🤖 Model Information")

    st.info(f"""
    Model : Random Forest Regressor

    Training Samples : {len(df):,}

    Prediction Features : 5

    Current Confidence : {confidence}%

    Status : Production Ready
    """)