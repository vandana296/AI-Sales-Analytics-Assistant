import pandas as pd


# ---------------------------------------------------
# Overall KPIs
# ---------------------------------------------------

def calculate_kpis(df):

    total_sales = df["Sales"].sum()

    total_profit = df["Profit"].sum()

    total_orders = df["Order ID"].nunique()

    profit_margin = (
        (total_profit / total_sales) * 100
        if total_sales > 0
        else 0
    )

    avg_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    return {
        "Total Sales": total_sales,
        "Total Profit": total_profit,
        "Total Orders": total_orders,
        "Profit Margin": profit_margin,
        "Average Order Value": avg_order_value
    }


# ---------------------------------------------------
# Category Performance
# ---------------------------------------------------

def category_performance(df):

    category_df = (
        df.groupby("Category")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    return category_df


# ---------------------------------------------------
# Sub-Category Performance
# ---------------------------------------------------

def subcategory_performance(df):

    sub_df = (
        df.groupby("Sub-Category")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    return sub_df


# ---------------------------------------------------
# Regional Performance
# ---------------------------------------------------

def regional_performance(df):

    region_df = (
        df.groupby("Region")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    return region_df


# ---------------------------------------------------
# Segment Performance
# ---------------------------------------------------

def segment_performance(df):

    segment_df = (
        df.groupby("Segment")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    return segment_df


# ---------------------------------------------------
# Top Products
# ---------------------------------------------------

def top_products(df, top_n=10):

    top_df = (
        df.groupby("Product Name")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
        .head(top_n)
    )

    return top_df


# ---------------------------------------------------
# Loss Making Products
# ---------------------------------------------------

def loss_products(df, top_n=10):

    loss_df = (
        df.groupby("Product Name")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values("Profit")
        .head(top_n)
    )

    return loss_df


# ---------------------------------------------------
# Monthly Performance
# ---------------------------------------------------

def monthly_performance(df):

    data = df.copy()

    data["Order Date"] = pd.to_datetime(data["Order Date"])

    data["Month"] = (
        data["Order Date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly = (
        data.groupby("Month")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique")
        )
        .reset_index()
    )

    return monthly


# ---------------------------------------------------
# Best Category
# ---------------------------------------------------

def best_category(df):

    return (
        category_performance(df)
        .iloc[0]
    )


# ---------------------------------------------------
# Worst Category
# ---------------------------------------------------

def worst_category(df):

    return (
        category_performance(df)
        .sort_values("Profit")
        .iloc[0]
    )


# ---------------------------------------------------
# Best Region
# ---------------------------------------------------

def best_region(df):

    return (
        regional_performance(df)
        .iloc[0]
    )


# ---------------------------------------------------
# Worst Region
# ---------------------------------------------------

def worst_region(df):

    return (
        regional_performance(df)
        .sort_values("Profit")
        .iloc[0]
    )