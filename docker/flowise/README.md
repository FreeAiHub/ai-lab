# Flowise — Visual AI Agent Builder

> Build LangChain agents, RAG pipelines, chatbots — drag & drop, no code needed.

## Start

```bash
cp .env.example .env
# Add your OpenAI key to .env
docker compose up -d
```

Open → http://localhost:3000

## What to build (in order)

1. **Simple LLM chain** — just ask Claude/GPT a question
2. **Document Q&A** — upload PDF, ask questions (basic RAG)
3. **Agent with tools** — web search + calculator
4. **Memory chatbot** — conversation with history

## Build your first RAG flow

```
Flowise UI → New Flow
  └── PDF File Loader
  └── Recursive Text Splitter (chunk: 500)
  └── OpenAI Embeddings
  └── In-Memory Vector Store
  └── Conversational Retrieval QA Chain
  └── ChatOpenAI (gpt-4o-mini)
```

## Save flows to Git

```bash
# Export from Flowise UI → JSON → save here:
mkdir -p flows/
# git add flows/ && git commit -m "Add: FAQ chatbot flow"
```

## Stop
```bash
docker compose down
docker compose down -v  # also delete data
```
