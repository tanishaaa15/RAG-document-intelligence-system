#  RAG (Retrieval-Augmented Generation) Document QA App

This is a full-stack **RAG (Retrieval-Augmented Generation)** application built with **FastAPI**, **Gradio**, and **Groq** (LLama3). The app allows users to upload documents (PDF, DOCX, TXT, HTML), ask natural language questions, and receive context-based answers.

---

##  Features

-  Supports document upload: `.pdf`, `.docx`, `.txt`, `.html`
-  Automatically extracts and chunks text
-  Generates embeddings using `sentence-transformers`
-  Stores and retrieves relevant chunks from `FAISS` vector database
-  Uses `Groq` with LLama3 for answering questions with real-time context
-  FastAPI backend + Gradio frontend

---

## Working
1. Document Upload: File is uploaded and text is extracted based on file type.
2. Chunking: Long texts are split into overlapping chunks for better semantic embedding.
3. Embedding: Each chunk is embedded using all-MiniLM-L6-v2 from sentence-transformers.
4. Vector Store: Embeddings are stored in a FAISS vector DB with optional tags.
5. Querying: On a question, top relevant chunks are retrieved using semantic similarity.
6. Answer Generation: Prompt is built with chunks and sent to Groq’s LLama3 via API.
7. Gradio UI: All interactions are available in a simple web UI.

---

##  Project Structure
rag_app/

├──app/

│ ├──main.py # FastAPI app with endpoints

│ ├──document_processor.py # File reading and text chunking logic

│ ├──vector_store.py # FAISS logic: embedding, storage, retrieval

│ ├──embedding.py # Embedding generator using SentenceTransformer

│ ├──llm.py # Groq API integration (LLama3)

├──gradio_app

│ ├──ui.py # Gradio frontend (upload + question UI)

├──uploaded_files

├──groq_api_key.txt

├──requirements.txt # Python dependencies

└──README.md # Project documentation

---

## Installation
1. installing requirements: pip install -r requirements.txt
2. Start the FastAPI backend with the command in cmd: uvicorn app.main:app --reload, then go to http://127.0.0.1:8000 (or the link it shows in cmd)
3. For gradio interface, run command in cmd: python gradio_app\ui.py, Then go to: http://localhost:7860

---



