# ai-lab: Docker Compose stacks for learning AI agents and RAG

Five `docker compose` stacks I use to learn agent and RAG tooling locally, plus four written
project briefs. The stacks are configuration, not applications: they run other people's
software.

## Status

Stacks are configured; no learning project has code yet.

The repository used to commit a log line five days a week to keep the contribution
graph green. That workflow was removed on 2026-09-22, and the log it wrote is still
here as a record of it. The last commit that added real content is 2026-03-17.

## What is in the repository

- Five Compose stacks, each in its own directory with its own README:
  - `docker/flowise/`: Flowise on port 3000. Confirmation: `docker/flowise/docker-compose.yml`.
  - `docker/n8n/`: n8n on port 5678. Confirmation: `docker/n8n/docker-compose.yml`.
  - `docker/open-webui/`: Open WebUI on port 8080 with Ollama on 11434.
    Confirmation: `docker/open-webui/docker-compose.yml`.
  - `docker/qdrant/`: Qdrant on ports 6333 and 6334. Confirmation:
    `docker/qdrant/docker-compose.yml`.
  - `docker/full-stack/`: all four together. Confirmation: `docker/full-stack/docker-compose.yml`.
- Every stack runs third-party images from Docker Hub or GitHub Container Registry. Own code
  here is limited to the Compose files and the two workflows.
- `docker/flowise/.env.example` and `docker/full-stack/.env.example` ship an API-key
  template. The n8n, Open WebUI and Qdrant stacks need no key to start; Open WebUI and
  Ollama run models locally.
- Four project briefs with setup steps and code listings: `projects/01-faq-chatbot/README.md`,
  `projects/02-rag-pdf/README.md`, `projects/03-agent-websearch/README.md`,
  `projects/04-n8n-email-ai/README.md`.
- Two GitHub Actions workflows: `daily-activity.yml` appends a date-stamped line to
  `logs/activity.log` on weekdays, `learning-tracker.yml` regenerates `PROGRESS.md` from the
  contents of `projects/`.

## Quick start

Any single stack:

```bash
git clone https://github.com/FreeAiHub/ai-lab.git
cd ai-lab/docker/flowise
cp .env.example .env       # add OPENAI_API_KEY, or use Open WebUI with Ollama instead
docker compose up -d
# → http://localhost:3000
```

All of it at once:

```bash
cd docker/full-stack
cp .env.example .env
docker compose up -d
```

Confirmed against `docker/flowise/README.md` and `docker/full-stack/docker-compose.yml`.
The full stack expects 16GB of RAM, per the comment at the top of that file.

Ports, taken from the Compose files rather than guessed:

| Stack | Ports |
|---|---|
| Flowise | 3000 |
| n8n | 5678 |
| Open WebUI + Ollama | 8080, 11434 |
| Qdrant | 6333 (HTTP), 6334 (gRPC) |

## How the full stack fits together

```
open-webui :8080 ──► ollama :11434        local models, no API key
flowise    :3000 ──► qdrant :6333         visual agent builder, vectors in Qdrant
                 └─► ollama :11434
n8n        :5678 ──► qdrant :6333         automation workflows
```

Each service declares `depends_on` for the ones it needs, so `docker compose up -d` starts
them in order. `docker/full-stack/docker-compose.yml` is the file to read for the wiring.

## What is not here yet

- No project code. `PROGRESS.md` reports 0 of 4 projects complete, and `projects/` contains
  only README files. The briefs are instructions to follow, not finished work.
- Dify is in the earlier README as a stack on port 80 with 4GB of RAM. There is no
  `docker/dify/` directory, so it is not here.
- `projects/05-custom-rag/` was listed as a fifth project. It does not exist.
- `docker/full-stack/` has no README of its own; the Compose file is the documentation.
- No tests, no linting, no CI beyond one workflow that rebuilds `PROGRESS.md` when
  `projects/**` changes.
- No `LICENSE` file. The repository is public, so the default terms apply.
- `logs/activity.log` counts files, not work. All 133 entries since 2026-03-18 read
  "Files in repo: 21", while the sync kept running. That is why this README dates the
  content, not the last commit.
