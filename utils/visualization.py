import pandas as pd
import plotly.express as px


# --------------------------------------------------
# Monthly Sales Trend
# --------------------------------------------------

def monthly_sales(df):

    data = df.copy()

    if "Order Date" in data.columns:
        data["Order Date"] = pd.to_datetime(data["Order Date"])
        data["Month"] = data["Order Date"].dt.to_period("M").astype(str)

    elif "Order Date" not in data.columns and "Month" not in data.columns:
        return px.line(title="Order Date column not found")

    monthly = (
        data.groupby("Month", as_index=False)["Sales"]
        .sum()
    )

    fig = px.line(
        monthly,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend",
    )

    return fig


# --------------------------------------------------
# Sales by Category
# --------------------------------------------------

def sales_by_category(df):

    category = (
        df.groupby("Category", as_index=False)["Sales"]
        .sum()
    )

    fig = px.bar(
        category,
        x="Category",
        y="Sales",
        title="Sales by Category",
        text_auto=".2s",
    )

    return fig


# --------------------------------------------------
# Sales by Region
# --------------------------------------------------

def sales_by_region(df):

    region = (
        df.groupby("Region", as_index=False)["Sales"]
        .sum()
    )

    fig = px.pie(
        region,
        names="Region",
        values="Sales",
        title="Sales by Region",
    )

    return fig


# --------------------------------------------------
# Profit by Segment
# --------------------------------------------------

def profit_by_segment(df):

    segment = (
        df.groupby("Segment", as_index=False)["Profit"]
        .sum()
    )

    fig = px.bar(
        segment,
        x="Segment",
        y="Profit",
        title="Profit by Segment",
        color="Segment",
        text_auto=".2s",
    )

    return fig


# --------------------------------------------------
# Top 10 Products
# --------------------------------------------------

def top_products(df):

    if "Product Name" not in df.columns:
        return px.bar(
            title="Product Name column not found in dataset"
        )

    top = (
        df.groupby("Product Name", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top 10 Products by Sales",
        text_auto=".2s",
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        height=500,
    )

    return fig