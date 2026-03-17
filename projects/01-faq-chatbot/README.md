# Project 1: FAQ Chatbot with Flowise

**Goal:** Build RAG chatbot using visual interface, no code  
**Time:** 1-2 hours  
**Stack:** Flowise (drag & drop)

---

## Steps

### 1. Start Flowise
```bash
cd ../../docker/flowise
docker compose up -d
# Open http://localhost:3000
```

### 2. Build flow

```
Nodes to add and connect:

[PDF File Loader]
      ↓
[Recursive Text Splitter]  ← chunk_size: 500, overlap: 50
      ↓
[OpenAI Embeddings]        ← model: text-embedding-3-small
      ↓
[In-Memory Vector Store]
      ↓
[Conversational Retrieval QA Chain]
      ↑                    ↑
[ChatOpenAI]          [Buffer Memory]
```

### 3. Test
- Upload any PDF (product manual, article)
- Ask questions in chat widget

### 4. Save to Git
```bash
# Export flow: Flowise UI → ⋮ → Export
mv ~/Downloads/*.json ./faq-chatbot-flow.json
git add . && git commit -m "✅ Project 1 complete: FAQ chatbot"
```

## What you learned
- Document chunking (why 500 tokens?)
- Embeddings (text → vector)
- Vector similarity search
- RAG chain: retrieve → augment → generate

## ➡️ Next: [Project 2 — RAG in Python](../02-rag-pdf/)
