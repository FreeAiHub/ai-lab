# Project 2: RAG over PDF — Python from scratch

**Goal:** Build RAG without UI — understand every single step  
**Time:** 3-4 hours  
**Stack:** Python + Qdrant + OpenAI

---

## Setup

```bash
# Start Qdrant
cd ../../docker/qdrant
docker compose up -d

# Python environment
python3 -m venv venv
source venv/bin/activate
pip install qdrant-client openai langchain langchain-community pypdf python-dotenv

# Create .env
echo 'OPENAI_API_KEY=sk-your-key' > .env
```

## Code: rag_pipeline.py

```python
from pathlib import Path
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import openai, os, uuid
from dotenv import load_dotenv

load_dotenv()
oai = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = QdrantClient(url="http://localhost:6333")
COLLECTION = "pdf_docs"


def setup():
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION not in collections:
        client.create_collection(
            COLLECTION,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
    print(f"✅ Qdrant collection ready: {COLLECTION}")


def embed(text: str) -> List[float]:
    return oai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding


def ingest_pdf(pdf_path: str):
    """Load PDF → split → embed → store in Qdrant"""
    print(f"\n📄 Loading: {pdf_path}")
    docs = PyPDFLoader(pdf_path).load()
    
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)
    print(f"✂️  {len(chunks)} chunks created")
    
    # Embed and store
    points = []
    for i, chunk in enumerate(chunks):
        vector = embed(chunk.page_content)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": chunk.page_content,
                "source": pdf_path,
                "page": chunk.metadata.get("page", 0),
                "chunk_index": i
            }
        ))
    
    client.upsert(collection_name=COLLECTION, points=points)
    print(f"✅ Stored {len(points)} chunks in Qdrant")


def ask(question: str, top_k: int = 3) -> str:
    """RAG: embed question → retrieve chunks → generate answer"""
    
    # Step 1: embed the question
    q_vector = embed(question)
    
    # Step 2: find similar chunks in Qdrant
    results = client.search(
        collection_name=COLLECTION,
        query_vector=q_vector,
        limit=top_k
    )
    
    if not results:
        return "No relevant content found."
    
    # Step 3: build context from retrieved chunks
    context_parts = []
    for r in results:
        context_parts.append(
            f"[Score: {r.score:.3f} | Page: {r.payload.get('page', 0)}]\n"
            f"{r.payload['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)
    
    # Step 4: generate answer with LLM
    response = oai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Answer questions based on the provided context. "
                           "If the answer is not in the context, say so honestly."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    setup()
    
    # Ingest PDF (put any PDF in this folder)
    pdf_files = list(Path(".").glob("*.pdf"))
    if pdf_files:
        for pdf in pdf_files:
            ingest_pdf(str(pdf))
    else:
        print("⚠️  No PDF files found. Put a PDF in this folder.")
        exit(1)
    
    print("\n🤖 RAG system ready! Ask questions (type 'q' to quit)\n")
    
    while True:
        question = input("❓ Question: ").strip()
        if question.lower() in ('q', 'quit', 'exit'):
            break
        if not question:
            continue
        print(f"\n💡 Answer: {ask(question)}\n")
```

## Run

```bash
# Put any PDF in this folder, then:
python rag_pipeline.py
```

## Experiments

1. Change `chunk_size` 500 → 200 — does quality change?
2. Change `top_k` 3 → 1 — worse answers?
3. Print `results[0].score` — understand similarity scoring
4. Try with your CV PDF from the CV repo

## ➡️ Next: [Project 3 — AI Agent](../03-agent-websearch/)
