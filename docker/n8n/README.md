# n8n — AI Automation Workflows

> Visual automation platform. Better than Make.com for self-hosted AI workflows.

## Start

```bash
cp .env.example .env
docker compose up -d
```

Open → http://localhost:5678

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
