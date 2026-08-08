import os
import streamlit as st

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings


# -----------------------------------------
# FAISS Storage Path
# -----------------------------------------

VECTOR_PATH = "models/faiss_index"


# -----------------------------------------
# Gemini Embedding Model
# -----------------------------------------

@st.cache_resource
def get_embedding_model():

    print("Loading Gemini embedding model...")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=st.secrets["GOOGLE_API_KEY"]
    )

    print("Gemini embedding model loaded")

    return embeddings


# -----------------------------------------
# Create / Load Vector Store
# -----------------------------------------

@st.cache_resource
def create_vector_store(df):

    embedding_model = get_embedding_model()

    # -------------------------------------
    # Load Existing FAISS Database
    # -------------------------------------

    if os.path.exists(VECTOR_PATH):

        print("Loading existing FAISS database...")

        vectorstore = FAISS.load_local(
            VECTOR_PATH,
            embedding_model,
            allow_dangerous_deserialization=True
        )

        print("FAISS database loaded successfully")

        return vectorstore

    # -------------------------------------
    # Create New FAISS Database
    # -------------------------------------

    print("Creating new FAISS database...")

    documents = []

    for index, row in df.iterrows():

        text = f"""
Sales Record {index}

{row.to_string()}
"""

        documents.append(
            Document(
                page_content=text
            )
        )

    print(
        f"Creating embeddings for {len(documents)} records..."
    )

    vectorstore = FAISS.from_documents(
        documents,
        embedding_model
    )

    # -------------------------------------
    # Save FAISS Database
    # -------------------------------------

    os.makedirs(
        "models",
        exist_ok=True
    )

    vectorstore.save_local(
        VECTOR_PATH
    )

    print(
        "FAISS database saved successfully"
    )

    return vectorstore


# -----------------------------------------
# Search Documents
# -----------------------------------------

def search_documents(
    vectorstore,
    question,
    k=5
):

    docs = vectorstore.similarity_search(
        question,
        k=k
    )

    return docs


# -----------------------------------------
# Prepare Context for Gemini
# -----------------------------------------

def prepare_context(docs):

    context = ""

    for i, doc in enumerate(docs):

        context += f"""
===== Record {i+1} =====

{doc.page_content}
"""

    return context