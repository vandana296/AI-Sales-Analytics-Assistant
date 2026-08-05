def build_context(df):

    return f"""
Rows: {len(df)}

Columns:
{list(df.columns)}

Total Sales:
{df["Sales"].sum():,.2f}

Total Profit:
{df["Profit"].sum():,.2f}

Top 10 Rows:

{df.head(10).to_string()}
"""