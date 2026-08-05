import plotly.express as px
import pandas as pd


def generate_chart(df, query):

    query = query.lower()

    # -----------------------------
    # Sales by Region
    # -----------------------------
    if "region" in query and "sales" in query:

        chart_df = (
            df.groupby("Region")["Sales"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            chart_df,
            x="Region",
            y="Sales",
            color="Sales",
            title="Sales by Region"
        )

        return fig, chart_df

    # -----------------------------
    # Profit by Category
    # -----------------------------
    elif "category" in query and "profit" in query:

        chart_df = (
            df.groupby("Category")["Profit"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            chart_df,
            x="Category",
            y="Profit",
            color="Profit",
            title="Profit by Category"
        )

        return fig, chart_df

    # -----------------------------
    # Sales by Segment
    # -----------------------------
    elif "segment" in query:

        chart_df = (
            df.groupby("Segment")["Sales"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            chart_df,
            values="Sales",
            names="Segment",
            title="Sales by Segment"
        )

        return fig, chart_df

    # -----------------------------
    # Monthly Sales Trend
    # -----------------------------
    elif "month" in query:

        data = df.copy()

        data["Order Date"] = pd.to_datetime(data["Order Date"])

        data["Month"] = data["Order Date"].dt.to_period("M").astype(str)

        chart_df = (
            data.groupby("Month")["Sales"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            chart_df,
            x="Month",
            y="Sales",
            markers=True,
            title="Monthly Sales Trend"
        )

        return fig, chart_df

    # -----------------------------
    # Top Products
    # -----------------------------
    elif "product" in query:

        chart_df = (
            df.groupby("Product Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            chart_df,
            x="Product Name",
            y="Sales",
            color="Sales",
            title="Top 10 Products"
        )

        return fig, chart_df

    # -----------------------------
    # Default
    # -----------------------------
    else:

        chart_df = (
            df.groupby("Category")["Sales"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            chart_df,
            x="Category",
            y="Sales",
            color="Sales",
            title="Sales by Category"
        )

        return fig, chart_df