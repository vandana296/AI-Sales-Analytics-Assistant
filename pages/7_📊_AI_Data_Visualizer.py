import streamlit as st

from utils.theme import load_theme
from utils.data_loader import (
    load_excel_data,
    find_main_dataset
)
from utils.chart_generator import generate_chart
from utils.gemini_helper import ask_gemini
from utils.chart_download import (
    download_chart_png,
    download_chart_html,
    download_chart_csv
)
from utils.theme import load_theme,show_header
# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="AI Data Visualization",
    page_icon="📊",
    layout="wide"
)

load_theme()

show_header("📊 AI Data Visualization")

st.markdown(
    """
Generate interactive business charts using natural language.

### Example Questions

- Show sales by region
- Monthly sales trend
- Profit by category
- Top 10 products
- Sales by segment
"""
)

st.divider()

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

try:

    sheets = load_excel_data()

    sheet_name, df = find_main_dataset(sheets)

except Exception as e:

    st.error(f"Unable to load dataset: {e}")

    st.stop()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.header("Dataset")

st.sidebar.success(sheet_name)

st.sidebar.write(f"Rows : {len(df):,}")
st.sidebar.write(f"Columns : {len(df.columns)}")

# -------------------------------------------------
# User Question
# -------------------------------------------------

question = st.text_input(
    "Ask your visualization question",
    placeholder="Example: Show sales by region"
)

# -------------------------------------------------
# Generate Visualization
# -------------------------------------------------

if st.button(
    "Generate Visualization",
    use_container_width=True
):

    if question.strip() == "":

        st.warning("Please enter a question.")

        st.stop()

    with st.spinner("Generating visualization..."):

        fig, chart_df = generate_chart(df, question)

    st.success("Visualization generated successfully!")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("📋 Data Used")

    st.dataframe(
        chart_df,
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------------------------
    # AI Insight
    # ---------------------------------------------

    st.subheader("🤖 AI Business Insight")

    context = chart_df.to_string(index=False)

    prompt = f"""
The user asked:

{question}

Business Data:

{context}

Generate:

1. Key insights
2. Business explanation
3. Actionable recommendations

Use bullet points.
Keep the response concise.
"""

    with st.spinner("Generating AI insights..."):

        insight = ask_gemini(
            prompt,
            context
        )

    st.markdown(insight)

    st.divider()

    # ---------------------------------------------
    # Downloads
    # ---------------------------------------------

    st.subheader("📥 Download")

    col1, col2, col3 = st.columns(3)

    with col1:

        download_chart_png(
            fig,
            "chart.png"
        )

    with col2:

        download_chart_html(
            fig,
            "chart.html"
        )

    with col3:

        download_chart_csv(
            chart_df,
            "chart_data.csv"
        )

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.divider()

st.caption(
    "🚀 GenAI Sales Analytics Assistant | AI Data Visualization"
)