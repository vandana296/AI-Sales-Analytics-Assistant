import pandas as pd

from utils.gemini_helper import ask_gemini


# ---------------------------------------------------
# Business Summary
# ---------------------------------------------------

def generate_business_summary(df):

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()

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

    best_segment = (
        df.groupby("Segment")["Profit"]
        .sum()
        .idxmax()
    )

    return f"""
### 📊 Business Summary

- **Total Sales:** £{total_sales:,.2f}

- **Total Profit:** £{total_profit:,.2f}

- **Total Orders:** {total_orders}

- **Highest Sales Region:** {best_region}

- **Best Category:** {best_category}

- **Most Profitable Segment:** {best_segment}
"""


# ---------------------------------------------------
# AI Executive Summary
# ---------------------------------------------------

def generate_executive_summary(
    kpis,
    category_df,
    region_df,
    segment_df,
    monthly_df,
    top_products_df,
    loss_products_df,
):

    context = f"""
====================================================
BUSINESS KPI
====================================================

{kpis}

====================================================
CATEGORY PERFORMANCE
====================================================

{category_df.to_string(index=False)}

====================================================
REGIONAL PERFORMANCE
====================================================

{region_df.to_string(index=False)}

====================================================
SEGMENT PERFORMANCE
====================================================

{segment_df.to_string(index=False)}

====================================================
MONTHLY PERFORMANCE
====================================================

{monthly_df.to_string(index=False)}

====================================================
TOP PRODUCTS
====================================================

{top_products_df.to_string(index=False)}

====================================================
LOSS MAKING PRODUCTS
====================================================

{loss_products_df.to_string(index=False)}
"""

    question = """
You are a Senior Business Intelligence Consultant.

Analyze ONLY the supplied business data.

Generate a professional Executive Business Report.

Use Markdown.

Include the following sections:

# Executive Summary

# KPI Highlights

# Sales Performance

# Profitability Analysis

# Category Analysis

# Regional Analysis

# Product Performance

# Risks

# Growth Opportunities

# Strategic Recommendations

Provide at least 8 actionable recommendations.

Do not invent information.

Use only the supplied data.
"""

    return ask_gemini(question, context)