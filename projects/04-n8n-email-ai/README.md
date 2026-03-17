# Project 4: n8n + AI Email Automation

**Goal:** Auto-process emails with AI, send summaries to Telegram  
**Time:** 2-3 hours  
**Stack:** n8n + OpenAI + Telegram Bot

---

## Setup

```bash
cd ../../docker/n8n
docker compose up -d
# Open http://localhost:5678
```

## Workflow 1: Email → AI Summary → Telegram

```
[Schedule: every 30 min]
  ↓
[Gmail: Get new emails]
  ↓
[Code node: filter important]
  ↓
[OpenAI: Summarize email + classify: urgent/normal/spam]
  ↓
[IF: urgent == true]
  YES → [Telegram: send with 🔴 prefix]
  NO  → [Telegram: send with ⚪ prefix]
```

## Workflow 2: Telegram Bot → AI → Response

```
[Telegram Trigger: new message]
  ↓
[OpenAI Chat: answer the question]
  ↓
[Telegram: send reply]
```

## How to create Telegram Bot

```
1. Open Telegram, find @BotFather
2. Send: /newbot
3. Set name: "Alexandre AI Assistant"
4. Set username: alexandre_ai_bot
5. Get TOKEN: 1234567890:ABCdef...

In n8n:
  Credentials → Telegram → Add
  Paste your token
```

## Save workflows to Git

```bash
mkdir -p workflows/
# n8n UI → workflow → ⋮ → Export → save JSON here
git add workflows/ && git commit -m "✅ Project 4: email AI workflow"
```
