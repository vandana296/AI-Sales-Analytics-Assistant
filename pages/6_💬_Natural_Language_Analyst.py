import streamlit as st
import plotly.express as px

from utils.data_loader import (
    load_excel_data,
    find_main_dataset
)

from utils.query_processor import process_query

from utils.gemini_helper import ask_gemini
from utils.theme import load_theme,show_header


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Natural Language Analyst",
    page_icon="💬",
    layout="wide"
)
load_theme()

show_header("💬 Natural Language Analyst")

st.markdown(
    """
Ask business questions in plain English.

Examples:

- Total Sales
- Total Profit
- Sales by Category
- Profit by Category
- Sales by Region
- Profit by Region
- Monthly Sales Trend
- Top Products
- Loss Making Products
- Sales by Segment
- Top Customers
"""
)

st.divider()


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

try:

    sheets = load_excel_data()

    sheet_name, df = find_main_dataset(sheets)

except Exception as e:

    st.error(e)
    st.stop()


# --------------------------------------------------
# User Input
# --------------------------------------------------

question = st.text_input(
    "Ask your business question"
)

# --------------------------------------------------
# Process Query
# --------------------------------------------------

if st.button("Analyze", use_container_width=True):

    if question.strip() == "":

        st.warning("Please enter a question.")

        st.stop()

    result, chart, title = process_query(question, df)

    # ------------------------------------------
    # Built-in Analytics
    # ------------------------------------------

    if result is not None:

        st.subheader(title)

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------
        # Bar Chart
        # ----------------------------

        if chart == "bar":

            x = result.columns[0]
            y = result.columns[1]

            fig = px.bar(
                result,
                x=x,
                y=y,
                title=title,
                text_auto=".2s"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------
        # Line Chart
        # ----------------------------

        elif chart == "line":

            x = result.columns[0]
            y = result.columns[1]

            fig = px.line(
                result,
                x=x,
                y=y,
                markers=True,
                title=title
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------
        # Pie Chart
        # ----------------------------

        elif chart == "pie":

            fig = px.pie(
                result,
                names=result.columns[0],
                values=result.columns[1],
                title=title
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ------------------------------------------
    # AI Fallback
    # ------------------------------------------

    else:

        st.info(
            "This question isn't supported by the built-in analytics. Asking Gemini AI..."
        )

        sample = df.head(100).to_string(index=False)

        answer = ask_gemini(
            question,
            sample
        )

        st.markdown(answer)