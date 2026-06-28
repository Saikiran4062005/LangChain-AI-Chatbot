import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# =====================================================
# LOAD EMBEDDING MODEL ONLY ONCE
# =====================================================

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


embeddings = get_embeddings()


# =====================================================
# CREATE VECTOR DATABASE
# =====================================================

@st.cache_resource(show_spinner=False)
def create_vectorstore(pdf_path):

    # Load PDF
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(docs)

    # Create FAISS Vector Store
    db = FAISS.from_documents(
        chunks,
        embeddings,
    )

    # Return both:
    # 1. FAISS database (semantic search)
    # 2. Original pages (page lookup)
    return db, docs