import streamlit as st
import tempfile
import time
import re

from chatbot import generate_answer
from gemini_chat import generate_gemini
from pdf_chat import create_vectorstore

# =====================================================
# PDF SYSTEM PROMPT
# =====================================================

PDF_SYSTEM_PROMPT = """
You answer ONLY using the uploaded PDF.

Rules:

- Never use outside knowledge.
- Never guess.
- If the answer is not found in the PDF, reply exactly:

I couldn't find that information in the uploaded PDF.
"""

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Lyca AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "pdf_pages" not in st.session_state:
    st.session_state.pdf_pages = None

# =====================================================
# LOAD CSS
# =====================================================

with open("styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🤖 Lyca AI")

    st.success("🟢 Online")

    st.caption("Powered by LangChain + Gemini + Groq")

    st.divider()

    # ------------------------
    # NEW CHAT
    # ------------------------

    if st.button(
        "➕ New Chat",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.rerun()

    st.divider()

    # ------------------------
    # PDF UPLOAD
    # ------------------------

    uploaded_pdf = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"],
    )

    if (
        uploaded_pdf is not None
        and st.session_state.vector_db is None
    ):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as tmp:

            tmp.write(uploaded_pdf.read())

            with st.spinner("📖 Reading PDF..."):

                (
                    st.session_state.vector_db,
                    st.session_state.pdf_pages,
                ) = create_vectorstore(
                    tmp.name
                )

        st.success(f"✅ {uploaded_pdf.name}")

    # ------------------------
    # REMOVE PDF
    # ------------------------

    if st.session_state.vector_db is not None:

        if st.button(
            "🗑 Remove PDF",
            use_container_width=True,
        ):

            st.session_state.vector_db = None
            st.session_state.pdf_pages = None
            st.rerun()

    st.divider()

    st.markdown("### Capabilities")

    st.write("💻 Coding")
    st.write("📄 PDF Chat")
    st.write("🧠 AI Assistant")
    st.write("🌐 General Knowledge")

# =====================================================
# HERO
# =====================================================

st.markdown(
    """
<div class="hero">
<h1>🤖 Lyca AI</h1>
<p>Your Intelligent AI Assistant</p>
</div>
""",
    unsafe_allow_html=True,
)

# =====================================================
# FEATURE CARDS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

cards = [
    ("💻", "Code"),
    ("📚", "Study"),
    ("🧠", "AI"),
    ("📄", "PDF"),
]

for col, card in zip(
    [c1, c2, c3, c4],
    cards,
):

    with col:

        st.markdown(
            f"""
<div class="card">
<h3>{card[0]}</h3>
<b>{card[1]}</b>
</div>
""",
            unsafe_allow_html=True,
        )

st.divider()

# =====================================================
# WELCOME
# =====================================================

if not st.session_state.messages:

    st.info(
        "👋 Upload a PDF or start chatting."
    )

# =====================================================
# PREVIOUS CHAT
# =====================================================

for msg in st.session_state.messages:

    avatar = (
        "🧑"
        if msg["role"] == "user"
        else "🤖"
    )

    with st.chat_message(
        msg["role"],
        avatar=avatar,
    ):

        st.markdown(msg["content"])
# =====================================================
# CHAT INPUT
# =====================================================

prompt = st.chat_input("Message Lyca...")

if prompt:

    # ------------------------------------------
    # Detect whether the question is about the PDF
    # ------------------------------------------

    pdf_keywords = [
        "pdf",
        "document",
        "page",
        "chapter",
        "section",
        "according to",
        "from the pdf",
        "summarize",
        "summary",
        "explain this pdf",
        "what is the pdf about",
        "overview",
    ]

    is_pdf_query = (
        st.session_state.vector_db is not None
        and any(
            keyword in prompt.lower()
            for keyword in pdf_keywords
        )
    )

    # ------------------------------------------
    # Save user message
    # ------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message(
        "user",
        avatar="🧑",
    ):
        st.markdown(prompt)

    # ------------------------------------------
    # Assistant
    # ------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        placeholder = st.empty()

        answer = ""

        context = ""

        # =====================================================
        # PDF ROUTER
        # =====================================================

        if is_pdf_query:

            page_match = re.search(
                r"page\s+(\d+)",
                prompt.lower(),
            )

            # ------------------------------------------
            # Direct page lookup
            # ------------------------------------------

            if page_match:

                page = int(page_match.group(1)) - 1

                if (
                    0 <= page <
                    len(st.session_state.pdf_pages)
                ):

                    context = (
                        st.session_state
                        .pdf_pages[page]
                        .page_content
                    )

            # ------------------------------------------
            # PDF overview
            # ------------------------------------------

            elif (
                "what is the pdf about" in prompt.lower()
                or "summarize the pdf" in prompt.lower()
                or "overview of the pdf" in prompt.lower()
            ):

                context = "\n\n".join(

                    page.page_content

                    for page in st.session_state.pdf_pages[:5]

                )

            # ------------------------------------------
            # Semantic search
            # ------------------------------------------

            else:

                docs = (
                    st.session_state.vector_db
                    .max_marginal_relevance_search(
                        prompt,
                        k=5,
                        fetch_k=20,
                    )
                )

                context = "\n\n".join(

                    doc.page_content

                    for doc in docs

                )
            # ------------------------------------------
            # Build PDF Prompt
            # ------------------------------------------

            pdf_prompt = f"""
You are Lyca AI.

Answer ONLY using the uploaded PDF.

Rules:

1. Never use outside knowledge.
2. Never guess.
3. If the answer is not present in the PDF, reply EXACTLY:

I couldn't find that information in the uploaded PDF.

---------------- PDF ----------------

{context}

-------------------------------------

Question:

{prompt}

Answer:
"""

            answer = generate_answer(
                [
                    {
                        "role": "user",
                        "content": pdf_prompt,
                    }
                ],
                system_prompt=PDF_SYSTEM_PROMPT,
            )

        # =====================================================
        # GENERAL AI
        # =====================================================

        else:

            answer = generate_gemini(
                st.session_state.messages
            )

        # =====================================================
        # Streaming Response
        # =====================================================

        stream = ""

        for word in answer.split():

            stream += word + " "

            placeholder.markdown(
                stream + "▌"
            )

            time.sleep(0.02)

        placeholder.markdown(stream)
    # =====================================================
    # SAVE ASSISTANT MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )