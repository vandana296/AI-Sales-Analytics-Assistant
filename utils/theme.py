import streamlit as st
from pathlib import Path


# -------------------------------------------------
# Load CSS Theme
# -------------------------------------------------

def load_theme():

    with open("assets/style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


# -------------------------------------------------
# Professional Header
# -------------------------------------------------

def show_header(title, subtitle="AI Powered Business Intelligence Platform"):

    BASE_DIR = Path(__file__).resolve().parent.parent

    logo_path = BASE_DIR / "assets" / "logo.png"

    col1, col2 = st.columns([1.5, 5])

    with col1:

        if logo_path.exists():

            st.image(
                str(logo_path),
                width=140
            )

    with col2:

        st.title(title)

        st.caption(subtitle)

    st.divider()
