import streamlit as st

from utils.data_loader import (
    load_excel_data,
    find_main_dataset
)

from utils.chat_memory import (
    initialize_chat,
    add_message,
    get_messages
)

from utils.rag import (
    create_vector_store,
    search_documents,
    prepare_context
)

from utils.gemini_helper import ask_gemini
from utils.theme import load_theme, show_header


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Business Copilot",
    page_icon="🤖",
    layout="wide"
)

load_theme()

show_header("🤖 AI Business Copilot - RAG Assistant")

st.markdown("""
Ask questions about your sales data.

### Example Questions

- Which region has highest sales?
- Which product generates maximum profit?
- Why is profit decreasing?
- Give business recommendations.
""")

st.divider()

# ---------------------------------------------------
# Initialize Chat
# ---------------------------------------------------

initialize_chat()

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

try:

    sheets = load_excel_data()

    sheet_name, df = find_main_dataset(sheets)

    if df is None:

        st.error("❌ No suitable dataset found")

        st.stop()

except Exception as e:

    st.error(f"Dataset loading error: {e}")

    st.stop()

# ---------------------------------------------------
# Create RAG Vector Store
# ---------------------------------------------------

with st.spinner("Creating AI Knowledge Base..."):

    vectorstore = create_vector_store(df)

st.success("✅ AI Knowledge Base Ready")

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.title("🤖 AI Copilot")

st.sidebar.success("Gemini + RAG + FAISS")

st.sidebar.write(f"**Dataset:** {sheet_name}")
st.sidebar.write(f"**Rows:** {len(df):,}")
st.sidebar.write(f"**Columns:** {len(df.columns)}")

st.sidebar.divider()

# Download Chat

if get_messages():

    chat_text = ""

    for msg in get_messages():

        role = "You" if msg["role"] == "user" else "AI"

        chat_text += f"{role}:\n{msg['content']}\n\n"

    st.sidebar.download_button(

        "📥 Download Chat",

        data=chat_text,

        file_name="AI_Conversation.txt",

        mime="text/plain",

        use_container_width=True

    )

# Clear Chat

if st.sidebar.button(

    "🗑 Clear Chat",

    use_container_width=True

):

    st.session_state.messages = []

    st.rerun()

# ---------------------------------------------------
# Quick Questions
# ---------------------------------------------------

st.subheader("💡 Quick Questions")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button("📊 Business Summary"):

        st.session_state.question = "Give me a complete business summary."

with col2:

    if st.button("🏆 Best Product"):

        st.session_state.question = "Which product has the highest sales?"

with col3:

    if st.button("💡 Recommendations"):

        st.session_state.question = "Give me five business recommendations."

# ---------------------------------------------------
# Chat History
# ---------------------------------------------------

for message in get_messages():

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------------------------------------------
# User Question
# ---------------------------------------------------

question = st.chat_input("Ask your business question...")

if "question" in st.session_state:

    question = st.session_state.question

    del st.session_state.question

# ---------------------------------------------------
# AI Response
# ---------------------------------------------------

if question:

    add_message("user", question)

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("🤖 Gemini AI is analyzing your business..."):

            try:

                docs = search_documents(
                    vectorstore,
                    question,
                    k=5
                )

                context = prepare_context(docs)

                response = ask_gemini(question, context)

            except Exception as e:

                response = f"❌ AI Error: {e}"

            st.markdown(response)

    add_message("assistant", response)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.divider()

st.caption(
    "🚀 AI Sales Analytics Assistant | Gemini + RAG + FAISS"
)