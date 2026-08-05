import streamlit as st
import pandas as pd

from utils.data_loader import load_excel_data, find_main_dataset
from utils.theme import load_theme,show_header

st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)
load_theme()

show_header("📄 Reports Center")
st.markdown("Download your business data and reports.")

# ---------------------------------
# Load Dataset
# ---------------------------------

try:
    sheets = load_excel_data()
    sheet_name, df = find_main_dataset(sheets)

except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ---------------------------------
# Report Summary
# ---------------------------------

st.subheader("📊 Report Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Rows", len(df))
col2.metric("Columns", len(df.columns))
col3.metric("Sheet", sheet_name)

st.markdown("---")

# ---------------------------------
# Preview
# ---------------------------------

st.subheader("Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# ---------------------------------
# Download CSV
# ---------------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Dataset (CSV)",
    data=csv,
    file_name="superstore_data.csv",
    mime="text/csv"
)

# ---------------------------------
# PDF Report
# ---------------------------------

st.info("📄 PDF Report generation is available from the Dashboard page.")

st.markdown("---")

st.success("Reports module is working successfully.")