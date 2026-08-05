import streamlit as st
import plotly.io as pio
from utils.theme import load_theme

pio.templates.default = "plotly_white"

st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="📊",
    layout="wide"
)
load_theme()

# Sidebar
st.sidebar.image(
    "assets/logo.png",
    width=180
)

st.sidebar.markdown("## AI Sales Analytics Assistant")
st.sidebar.caption("Business Intelligence Platform")
st.sidebar.markdown("---")
st.title("📊 AI Business Intelligence Assistant")

st.markdown("""
## Welcome 👋

This application provides:

- 📊 Dashboard
- 📈 Interactive Visualizations
- 🤖 AI Business Assistant
- 📉 Sales Prediction
- 📄 Report Generation

Use the **sidebar** to navigate between pages.
""")