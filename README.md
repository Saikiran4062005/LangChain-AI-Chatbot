# 🤖 Lyca AI

An intelligent AI chatbot built with **Streamlit**, **LangChain**, **Google Gemini**, **Groq**, and **FAISS**. 
Lyca AI provides natural conversations, real-time AI responses, and intelligent PDF question answering using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

### 💬 General AI Chat
- Natural conversations powered by Google Gemini
- Coding assistance
- Mathematics & science explanations
- Writing and brainstorming
- Conversation memory

### 📄 Chat with PDF
- Upload PDF documents
- Ask questions about the uploaded PDF
- Semantic search using FAISS vector database
- Page-specific search
- PDF summarization
- Answers generated only from the uploaded document

### ⚡ AI Technologies
- Google Gemini for general conversations
- Groq Llama 3.3 70B for PDF reasoning
- LangChain for orchestration
- HuggingFace Embeddings
- FAISS Vector Store

---

# 🖥️ Built With

- Python
- Streamlit
- LangChain
- Google Gemini API
- Groq API
- HuggingFace Transformers
- FAISS
- PyPDFLoader

---

# 📂 Project Structure

```
LangChain-AI-Chatbot/
│
├── app.py
├── chatbot.py
├── gemini_chat.py
├── pdf_chat.py
├── prompts.py
├── styles.css
├── requirements.txt
├── .gitignore
├── README.md
└── assets/
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Saikiran4062005/LangChain-AI-Chatbot.git
```

Move into the project

```bash
cd LangChain-AI-Chatbot
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

---

# 💡 Example Prompts

### General AI

- Explain recursion in Python.
- Write a Java program for Binary Search.
- Explain TCP/IP.
- What's the latest AI news?

### PDF Chat

- What is this PDF about?
- Summarize the document.
- Explain DNS according to the PDF.
- What is mentioned on page 15?
- Give important points from Chapter 3.

---

# 🌟 Highlights

- AI Chat Assistant
- Retrieval-Augmented Generation (RAG)
- PDF Question Answering
- Semantic Search
- Conversation Memory
- Modern Streamlit UI
- Real-time AI Responses
- Fast Vector Search with FAISS

---



---

# 🔮 Future Improvements

- Multiple PDF support
- Image understanding
- Voice assistant
- Export chat history
- Dark/Light themes
- OCR support
- PDF citations
- Multi-language support

---

# 👨‍💻 Author

**Sai Kiran**

B.Tech Information Technology

GitHub:
https://github.com/Saikiran4062005

---

# ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future improvements.
