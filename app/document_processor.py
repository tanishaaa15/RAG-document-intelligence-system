import os
import fitz  # PyMuPDF
import docx
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util

# =========================
# 📄 Extract Text by File Type
# =========================

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = "\n".join([page.get_text() for page in doc])
    doc.close()
    return text

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_text_from_html(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")
        return soup.get_text(separator="\n")

# =========================
# ✂️ Chunking Logic
# =========================

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# =========================
# 🤖 Embedding Model
# =========================

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Store chunks and embeddings in memory
stored_chunks = []
stored_embeddings = []

# =========================
# 🚀 Master Function
# =========================

def process_file(file_path, chunk_size=300):
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)
        elif ext == ".docx":
            text = extract_text_from_docx(file_path)
        elif ext == ".txt":
            text = extract_text_from_txt(file_path)
        elif ext == ".html":
            text = extract_text_from_html(file_path)
        else:
            raise ValueError(f"❌ Unsupported file type: {ext}")

        print(f"✅ Extracted text from {ext.upper()} ({len(text)} characters)")

        chunks = chunk_text(text, chunk_size=chunk_size)
        print(f"✂️ Generated {len(chunks)} text chunks.")

        # Generate and store embeddings
        embeddings = embedding_model.encode(chunks, show_progress_bar=True)
        stored_chunks.extend(chunks)
        stored_embeddings.extend(embeddings)

        return chunks

    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return []

# =========================
# 🔍 Chunk Retrieval Function
# =========================

def retrieve_relevant_chunks(query, top_k=3):
    if not stored_embeddings:
        return ["❌ No documents uploaded yet."]
    
    query_embedding = embedding_model.encode([query])[0]
    similarities = util.cos_sim(query_embedding, stored_embeddings)[0]

    top_indices = similarities.argsort(descending=True)[:top_k]
    top_chunks = [stored_chunks[i] for i in top_indices]

    return top_chunks
