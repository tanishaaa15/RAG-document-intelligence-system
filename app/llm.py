# ✅ llm.py (Groq Integration)

import requests
import os

# ✅ Load Groq API key securely from text file
def get_groq_api_key():
    try:
        with open("groq_key.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        raise ValueError("❌ groq_api_key.txt not found. Please create it and paste your API key.")

GROQ_API_KEY = get_groq_api_key()

# ✅ Generate answer from context using Groq

def generate_answer_with_groq(query, context):
    prompt = f"""Answer the user's question using only the provided context.
If the answer is not found in the context, say \"I don't know based on the context.\"

Context:
{context}

Question:
{query}

Answer:"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
    )

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# ✅ Optional alias if main.py is expecting 'generate_answer'
generate_answer = generate_answer_with_groq
