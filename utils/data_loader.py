import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data
def load_excel_data():
    """
    Load all sheets from the Excel workbook.
    """

    BASE_DIR = Path(__file__).resolve().parent.parent
    file_path = BASE_DIR / "data" / "Superstore Dataset.xlsx"

    sheets = pd.read_excel(
        file_path,
        sheet_name=None
    )

    return sheets


@st.cache_data
def find_main_dataset(sheets):
    """
    Automatically detect the main sales dataset.
    """

    required_columns = {
        "Sales",
        "Profit",
        "Category",
        "Region",
        "Segment"
    }

    for sheet_name, df in sheets.items():

        if required_columns.issubset(df.columns):
            return sheet_name, df

    return None, None