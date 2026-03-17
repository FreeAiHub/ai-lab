# 🤖 AI Lab — Personal AI Learning Environment

Docker-based stacks for learning AI Agents, RAG, and Automation in practice.

[![GitHub last commit](https://img.shields.io/github/last-commit/FreeAiHub/ai-lab?style=flat)](https://github.com/FreeAiHub/ai-lab)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat&logo=docker)](./docker/)

---

## 🗺️ Learning Roadmap

```
Week 1 → Flowise (Visual AI Agents — no code)
Week 2 → Dify (RAG + Agent platform)
Week 3 → n8n (Automation workflows with AI)
Week 4 → Open WebUI + Ollama (local LLMs, no API costs)
Week 5 → Build: custom RAG in Python + Qdrant
Week 6 → Build: Voice AI pipeline (Vapi + n8n)
```

---

## 🐳 Quick Start

```bash
git clone https://github.com/FreeAiHub/ai-lab.git
cd ai-lab

# Start with Flowise — easiest, visual UI, no code needed
cd docker/flowise
cp .env.example .env
# Edit .env — add OpenAI or OpenRouter key
docker compose up -d
# → Open http://localhost:3000
```

---

## 📦 Stacks

| Stack | Port | What it teaches | RAM needed |
|-------|------|-----------------|------------|
| [Flowise](./docker/flowise/) | 3000 | Visual AI Agents, LangChain | 2GB |
| [Dify](./docker/dify/) | 80 | RAG, prompts, agent platform | 4GB |
| [n8n](./docker/n8n/) | 5678 | AI automation workflows | 1GB |
| [Open WebUI](./docker/open-webui/) | 8080 | Local LLMs via Ollama | 8GB |
| [Qdrant](./docker/qdrant/) | 6333 | Vector DB for RAG | 512MB |
| [Full Stack](./docker/full-stack/) | various | Everything together | 16GB |

---

## 📚 Learning Projects

- [ ] [Project 1: FAQ Chatbot with Flowise](./projects/01-faq-chatbot/)
- [ ] [Project 2: RAG over PDF — Python from scratch](./projects/02-rag-pdf/)
- [ ] [Project 3: AI Agent with web search](./projects/03-agent-websearch/)
- [ ] [Project 4: n8n + AI email automation](./projects/04-n8n-email-ai/)
- [ ] [Project 5: Custom RAG pipeline production](./projects/05-custom-rag/)

---

## ⚙️ Requirements

- Docker Desktop (Mac/Windows) or Docker Engine (Linux)
- 8GB RAM minimum (16GB for full stack)
- OpenAI API key OR free OpenRouter key OR Ollama (local, free)

---

*Building in public — AI Agent & RAG learning journey*
