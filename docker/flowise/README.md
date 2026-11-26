# Flowise — Visual AI Agent Builder

> Build LangChain agents, RAG pipelines, chatbots — drag & drop, no code needed.

## Start

```bash
cp .env.example .env
# Set FLOWISE_PASSWORD in .env (required)
# Add your OpenAI key to .env
docker compose up -d
```

`FLOWISE_PASSWORD` is required: `docker compose up` fails if it is not set. The compose file loads `.env` as an optional `env_file`, so copy `.env.example` to `.env` first. `FLOWISE_USERNAME` defaults to `admin`.

Open → http://localhost:3000 and log in with those credentials.

## Ports

| Port | Service | Bound to |
|------|---------|----------|
| 3000 | Flowise UI + API | 127.0.0.1 (loopback only) |

The port is published on loopback only, so Flowise is not reachable from other machines.

## Remote access

Use an SSH tunnel instead of exposing the port:

```bash
ssh -L 3000:127.0.0.1:3000 user@your-server
# then open http://localhost:3000 on your machine
```

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
