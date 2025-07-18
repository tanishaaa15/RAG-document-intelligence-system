import gradio as gr
import requests

BACKEND_URL = "http://127.0.0.1:8000"

with gr.Blocks() as demo:
    gr.Markdown("## 🧠 RAG App: Upload a document and ask questions")

    with gr.Row():
        file_input = gr.File(label="Upload a file (PDF, DOCX, TXT, HTML)")
        upload_output = gr.Textbox(label="Upload Result")

    with gr.Row():
        question_input = gr.Textbox(label="Ask a question")
        answer_output = gr.Textbox(label="Answer")

    def upload_file(file):
        try:
            # ✅ FIX: Open the file in binary mode to read contents
            with open(file.name, "rb") as f:
                files = {"file": (file.name, f.read(), "application/octet-stream")}
                response = requests.post(f"{BACKEND_URL}/upload/", files=files, timeout=120)
                return response.json().get("message", "Error")
        except Exception as e:
            return f"❌ Error: {e}"

    def query_llm(question):
        try:
            response = requests.post(f"{BACKEND_URL}/query/", json={"question": question}, timeout=120)
            result = response.json()
            return result.get("answer", "No answer returned")
        except Exception as e:
            return f"❌ Error: {e}"

    file_input.change(fn=upload_file, inputs=[file_input], outputs=[upload_output])
    question_input.submit(fn=query_llm, inputs=[question_input], outputs=[answer_output])

demo.launch()
