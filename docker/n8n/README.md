# n8n — AI Automation Workflows

> Visual automation platform. Better than Make.com for self-hosted AI workflows.

## Start

```bash
cp .env.example .env
# Set N8N_PASSWORD in .env (required)
docker compose up -d
```

`N8N_PASSWORD` is required: `docker compose up` fails if it is not set, so copy `.env.example` to `.env` first. Basic auth is on; `N8N_USER` defaults to `admin`.

Open → http://localhost:5678 and log in with those credentials.

## Ports

| Port | Service | Bound to |
|------|---------|----------|
| 5678 | n8n UI + webhooks | 127.0.0.1 (loopback only) |

The port is published on loopback only, so n8n is not reachable from other machines.

## Remote access

Use an SSH tunnel instead of exposing the port:

```bash
ssh -L 5678:127.0.0.1:5678 user@your-server
# then open http://localhost:5678 on your machine
```

## AI Workflows to build

### 1. Telegram Bot + AI
```
Trigger: Telegram Message
  → OpenAI: Generate response
  → Telegram: Send reply
```

### 2. Email → AI Summary → Telegram
```
Trigger: Gmail new email (every 15 min)
  → OpenAI: Summarize email
  → Telegram: Send summary notification
```

### 3. Lead Qualification
```
Trigger: Webhook (form submit)
  → OpenAI: Score lead quality 1-10
  → If score > 7: HubSpot + Slack notify
  → If score < 7: auto-reply email
```

### 4. Document → RAG Ingestion
```
Trigger: File upload
  → Split into chunks
  → OpenAI Embeddings
  → Qdrant: store vectors
```

## Save workflows to Git

```bash
mkdir -p workflows/
# Export from n8n UI → JSON → save here
# git commit -m "Add: telegram bot workflow"
```
