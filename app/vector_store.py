from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# FAISS index and in-memory chunk store
dimension = 384  # embedding size for this model
index = faiss.IndexFlatL2(dimension)
chunk_list = []

def store_embeddings(chunks):
    """
    Store vector embeddings for document chunks.
    """
    global chunk_list
    embeddings = model.encode(chunks)
    index.add(np.array(embeddings).astype("float32"))
    chunk_list.extend(chunks)

def retrieve_relevant_chunks(query, top_k=3):
    """
    Retrieve top-k most relevant chunks for a query.
    """
    if not chunk_list:
        return []

    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding).astype("float32"), top_k)
    return [chunk_list[i] for i in I[0]]
