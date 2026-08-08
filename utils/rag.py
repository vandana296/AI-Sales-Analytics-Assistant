import os
import streamlit as st

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# =========================================================
# FAISS STORAGE PATH
# =========================================================

VECTOR_PATH = "models/faiss_index"


# =========================================================
# HUGGINGFACE EMBEDDING MODEL
# =========================================================

@st.cache_resource
def get_embedding_model():

    print("Loading HuggingFace embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding model loaded successfully")

    return embeddings


# =========================================================
# CREATE VECTOR STORE
# =========================================================

@st.cache_resource
def create_vector_store(df):

    embedding_model = get_embedding_model()

    print("Creating FAISS vector database...")

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

    print("FAISS vector database created successfully")

    return vectorstore


# =========================================================
# SEARCH DOCUMENTS
# =========================================================

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


# =========================================================
# PREPARE GEMINI CONTEXT
# =========================================================

def prepare_context(docs):

    context = ""

    for i, doc in enumerate(docs):

        context += f"""
==============================
RECORD {i + 1}
==============================

{doc.page_content}

"""

    return context