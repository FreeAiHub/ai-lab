"""Minimal RAG over a PDF: Qdrant for storage, Ollama for embeddings and answers.

Usage:
    python rag_pipeline.py path/to/file.pdf      # ingest, then ask questions
    python rag_pipeline.py --ask-only            # skip ingest, reuse the collection
"""
import os
import sys
import uuid

import requests
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

load_dotenv()

# Everything is configurable through environment variables (see .env.example).
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
CHAT_MODEL = os.getenv("CHAT_MODEL", "llama3.2")
COLLECTION = os.getenv("COLLECTION", "pdf_docs")

client = QdrantClient(url=QDRANT_URL)


def embed(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts with the Ollama /api/embed endpoint."""
    r = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={"model": EMBED_MODEL, "input": texts},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["embeddings"]


def ensure_collection(dim: int) -> None:
    """Create the collection if missing; vector size comes from the model."""
    if not client.collection_exists(COLLECTION):
        client.create_collection(
            COLLECTION,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )


def ingest_pdf(pdf_path: str) -> None:
    """Load PDF -> split into chunks -> embed -> upsert into Qdrant."""
    docs = PyPDFLoader(pdf_path).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"{len(chunks)} chunks from {pdf_path}")

    vectors = embed([c.page_content for c in chunks])
    ensure_collection(len(vectors[0]))
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vec,
            payload={
                "text": c.page_content,
                "source": pdf_path,
                "page": c.metadata.get("page", 0),
                "chunk_index": i,
            },
        )
        for i, (c, vec) in enumerate(zip(chunks, vectors))
    ]
    client.upsert(collection_name=COLLECTION, points=points)
    print(f"Stored {len(points)} chunks in '{COLLECTION}'")


def ask(question: str, top_k: int = 3) -> str:
    """Embed the question, retrieve the closest chunks, answer from them."""
    q_vec = embed([question])[0]
    # query_points replaces the deprecated client.search
    hits = client.query_points(
        collection_name=COLLECTION, query=q_vec, limit=top_k
    ).points
    if not hits:
        return "No relevant content found."

    context = "\n\n---\n\n".join(
        f"[Score: {h.score:.3f} | Page: {h.payload.get('page', 0)}]\n{h.payload['text']}"
        for h in hits
    )
    r = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": CHAT_MODEL,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": "Answer using only the provided context. "
                    "If the answer is not in the context, say so.",
                },
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
            ],
        },
        timeout=300,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] != "--ask-only":
        ingest_pdf(args[0])
    elif not args:
        sys.exit("Pass a PDF path, or --ask-only to query an existing collection.")

    print("Ready. Ask a question (q to quit).")
    while True:
        q = input("Question: ").strip()
        if q.lower() in ("q", "quit", "exit"):
            break
        if q:
            print(f"\nAnswer: {ask(q)}\n")
