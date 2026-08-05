import pandas as pd


# --------------------------------------------------
# Existing Intent Processor
# --------------------------------------------------

def execute_intent(df, intent):

    if intent == "highest_sales_category":

        return (
            df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

    elif intent == "highest_profit_region":

        return (
            df.groupby("Region")["Profit"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

    elif intent == "sales_by_segment":

        return (
            df.groupby("Segment")["Sales"]
            .sum()
            .reset_index()
        )

    elif intent == "monthly_sales":

        data = df.copy()

        data["Order Date"] = pd.to_datetime(data["Order Date"])

        data["Month"] = (
            data["Order Date"]
            .dt.to_period("M")
            .astype(str)
        )

        return (
            data.groupby("Month")["Sales"]
            .sum()
            .reset_index()
        )

    elif intent == "top_products":

        return (
            df.groupby("Product Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

    else:

        return df.head()


# --------------------------------------------------
# Natural Language Query Processor
# --------------------------------------------------

def process_query(question, df):

    question = question.lower().strip()

    chart = None
    title = ""

    # ----------------------------
    # Total Sales
    # ----------------------------

    if "total sales" in question:

        result = pd.DataFrame({

            "Metric": ["Total Sales"],

            "Value": [df["Sales"].sum()]

        })

        return result, None, "Total Sales"

    # ----------------------------
    # Total Profit
    # ----------------------------

    elif "total profit" in question:

        result = pd.DataFrame({

            "Metric": ["Total Profit"],

            "Value": [df["Profit"].sum()]

        })

        return result, None, "Total Profit"

    # ----------------------------
    # Sales by Category
    # ----------------------------

    elif "category" in question and "sales" in question:

        result = (
            df.groupby("Category")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
        )

        return result, "bar", "Sales by Category"

    # ----------------------------
    # Profit by Category
    # ----------------------------

    elif "category" in question and "profit" in question:

        result = (
            df.groupby("Category")["Profit"]
            .sum()
            .reset_index()
            .sort_values("Profit", ascending=False)
        )

        return result, "bar", "Profit by Category"

    # ----------------------------
    # Sales by Region
    # ----------------------------

    elif "region" in question and "sales" in question:

        result = (
            df.groupby("Region")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
        )

        return result, "bar", "Sales by Region"

    # ----------------------------
    # Profit by Region
    # ----------------------------

    elif "region" in question and "profit" in question:

        result = (
            df.groupby("Region")["Profit"]
            .sum()
            .reset_index()
            .sort_values("Profit", ascending=False)
        )

        return result, "bar", "Profit by Region"

    # ----------------------------
    # Monthly Sales
    # ----------------------------

    elif "monthly" in question and "sales" in question:

        data = df.copy()

        data["Order Date"] = pd.to_datetime(data["Order Date"])

        data["Month"] = (
            data["Order Date"]
            .dt.to_period("M")
            .astype(str)
        )

        result = (
            data.groupby("Month")["Sales"]
            .sum()
            .reset_index()
        )

        return result, "line", "Monthly Sales Trend"

    # ----------------------------
    # Top Products
    # ----------------------------

    elif "top" in question and "product" in question:

        result = (
            df.groupby("Product Name")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum")
            )
            .reset_index()
            .sort_values("Sales", ascending=False)
            .head(10)
        )

        return result, "bar", "Top Products"

    # ----------------------------
    # Loss Making Products
    # ----------------------------

    elif "loss" in question:

        result = (
            df.groupby("Product Name")
            .agg(
                Profit=("Profit", "sum")
            )
            .reset_index()
            .sort_values("Profit")
            .head(10)
        )

        return result, "bar", "Loss Making Products"

    # ----------------------------
    # Sales by Segment
    # ----------------------------

    elif "segment" in question:

        result = (
            df.groupby("Segment")["Sales"]
            .sum()
            .reset_index()
        )

        return result, "pie", "Sales by Segment"

    # ----------------------------
    # Top Customers
    # ----------------------------

    elif "customer" in question:

        result = (
            df.groupby("Customer Name")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
            .head(10)
        )

        return result, "bar", "Top Customers"

    # ----------------------------
    # Unknown
    # ----------------------------

    return None, None, None