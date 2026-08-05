import pandas as pd


def get_dataset_summary(df):
    """
    Returns important dataset statistics.
    """

    summary = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": df.isnull().sum().sum(),
        "Duplicate Rows": df.duplicated().sum(),
        "Memory Usage (MB)": round(df.memory_usage(deep=True).sum() / 1024**2, 2),
        "Numerical Columns": len(df.select_dtypes(include="number").columns),
        "Categorical Columns": len(df.select_dtypes(include="object").columns),
        "Date Columns": len(df.select_dtypes(include="datetime").columns)
    }

    return summary