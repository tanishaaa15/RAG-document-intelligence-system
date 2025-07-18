from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from app.document_processor import process_file
from app.vector_store import store_embeddings, retrieve_relevant_chunks
from app.llm import generate_answer

import os
import shutil
import uuid

app = FastAPI()
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "RAG API is up and running!"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

        # ✅ Save file to disk
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        print("📄 Processing document...")
        chunks = process_file(file_path)
        print(f"✂️ {len(chunks)} chunks created")

        if not chunks:
            return JSONResponse(content={"message": "No text extracted from document."}, status_code=400)

        store_embeddings(chunks)  # stores chunks to vector DB
        return {"message": "✅ File uploaded and processed successfully."}
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return JSONResponse(content={"message": f"Upload failed: {e}"}, status_code=500)

@app.post("/query/")
async def query(question: dict):
    try:
        query_text = question.get("question", "")
        if not query_text:
            return {"answer": "❌ No question provided."}

        relevant_chunks = retrieve_relevant_chunks(query_text)
        answer = generate_answer(query_text, relevant_chunks)

        return {"answer": answer}
    except Exception as e:
        print(f"❌ Query error: {e}")
        return {"answer": f"❌ Error: {e}"}
