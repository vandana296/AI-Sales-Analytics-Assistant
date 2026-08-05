import streamlit as st

from utils.database import initialize_database
from utils.auth import (
    create_default_admin,
    login_user
)

# --------------------------------------------------
# Initialize Database
# --------------------------------------------------

initialize_database()
create_default_admin()

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

# --------------------------------------------------
# Session
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# --------------------------------------------------
# Already Logged In
# --------------------------------------------------

if st.session_state.logged_in:

    st.success(
        f"Welcome {st.session_state.username}"
    )

    st.info(
        "You are already logged in."
    )

    st.success("Login Successful!")

    st.info("Please refresh the page or open the application from the sidebar.")

    st.stop()

    st.stop()

# --------------------------------------------------
# UI
# --------------------------------------------------

st.title("🔐 AI Sales Analytics")

st.subheader("Login")

username = st.text_input(
    "Username"
)

password = st.text_input(
    "Password",
    type="password"
)

# --------------------------------------------------
# Login Button
# --------------------------------------------------

if st.button(
    "Login",
    use_container_width=True
):

    user = login_user(
        username,
        password
    )

    if user:

        st.session_state.logged_in = True

        st.session_state.username = user["username"]

        st.session_state.role = user["role"]

        st.success("Login Successful!")

        st.rerun()

    else:

        st.error(
            "Invalid username or password."
        )

# --------------------------------------------------
# Default Credentials
# --------------------------------------------------

with st.expander("Default Login"):

    st.code(
"""
Username : admin

Password : admin123
"""
    )