# Full stack: Flowise + n8n + Qdrant + Ollama + Open WebUI

> Five services in one Compose file: a visual agent builder, a workflow tool, a vector
> database, a local model runtime and a chat UI.

Requires 16GB of RAM (recommended, per the comment at the top of `docker-compose.yml`).

## Start

```bash
cp .env.example .env
# Change the passwords, add API keys if you want to use hosted models
docker compose up -d
```

Open:

| Service | URL |
|---|---|
| Flowise | http://localhost:3000 |
| n8n | http://localhost:5678 |
| Open WebUI | http://localhost:8080 |
| Qdrant | http://localhost:6333 |
| Ollama API | http://localhost:11434 |

## What it runs

| Service | Image | Port | Volume |
|---|---|---|---|
| `qdrant` | `qdrant/qdrant:latest` | 6333 | `qdrant_storage` |
| `ollama` | `ollama/ollama:latest` | 11434 | `ollama_models` |
| `flowise` | `flowiseai/flowise:latest` | 3000 | `flowise_data` |
| `n8n` | `n8nio/n8n:latest` | 5678 | `n8n_data` |
| `open-webui` | `ghcr.io/open-webui/open-webui:main` | 8080 | `open_webui_data` |

All five use `restart: unless-stopped`. Only port 6333 is published for Qdrant; the gRPC
port 6334 from the standalone `docker/qdrant/` stack is not mapped here.

## How the services are wired

```
open-webui :8080 ──► ollama :11434
flowise    :3000 ──► qdrant :6333
                 └─► ollama :11434
n8n        :5678 ──► qdrant :6333
```

`depends_on` in the Compose file:

- `flowise` depends on `qdrant` and `ollama`
- `n8n` depends on `qdrant`
- `open-webui` depends on `ollama`

`depends_on` only controls start order. Nothing in the file waits for a service to be
ready, so a UI can come up a few seconds before the service it depends on.

Only Open WebUI is pointed at another service in the Compose file: it gets
`OLLAMA_BASE_URL=http://ollama:11434`. Flowise and n8n are not preconfigured to use Qdrant
or Ollama. Inside Flowise or n8n, use the service names (`http://qdrant:6333`,
`http://ollama:11434`) rather than `localhost`.

## Environment variables

Copy `.env.example` to `.env`. Compose reads `.env` from this directory.

| Variable | Used by | Default if unset |
|---|---|---|
| `FLOWISE_USERNAME` | Flowise login | `admin` |
| `FLOWISE_PASSWORD` | Flowise login | `flowise123` |
| `N8N_USER` | n8n basic auth user | `admin` |
| `N8N_PASSWORD` | n8n basic auth password | `n8n123` |
| `OPENAI_API_KEY` | Flowise and Open WebUI | empty |
| `ANTHROPIC_API_KEY` | Flowise | empty |

The defaults are weak. Set your own values in `.env`.

`.env.example` also lists `OPENROUTER_API_KEY`, but `docker-compose.yml` does not reference
it, so setting it has no effect on this stack.

API keys are optional. Ollama runs models locally without them.

n8n is started with `N8N_BASIC_AUTH_ACTIVE=true` and `WEBHOOK_URL=http://localhost:5678/`.

## Stop

```bash
docker compose down        # stop and remove containers, keep data
```

## Reset

```bash
docker compose down -v     # also delete all five named volumes
```

This removes everything in `qdrant_storage`, `ollama_models`, `flowise_data`, `n8n_data` and
`open_webui_data`, including downloaded Ollama models, saved flows and workflows.

To update images: `docker compose pull && docker compose up -d`. Most images use the
`latest` tag (Open WebUI uses `main`), so a pull can bring in breaking changes.

## Troubleshooting

- **Port already in use.** Ports 3000, 5678, 6333, 8080 and 11434 are published on the host.
  Stop whatever holds the port, or change the left-hand side of the mapping in
  `docker-compose.yml` (for example `"3001:3000"`).
- **Out of memory or the machine slows down.** The stack is sized for 16GB. Start fewer
  services, for example `docker compose up -d open-webui` starts only Open WebUI and
  Ollama.
- **Open WebUI shows no models.** The Ollama volume starts empty. Pull a model, for example
  `docker exec ollama ollama pull llama3.2`, then refresh.
- **Flowise or n8n cannot reach Qdrant or Ollama.** Use `http://qdrant:6333` and
  `http://ollama:11434`, not `localhost`, from inside those containers.
- **Cannot log in.** Check `.env`. If it is missing, the defaults in the table above apply.
  After changing credentials, run `docker compose up -d` again to recreate the containers.
- **See what is happening.** `docker compose ps` and `docker compose logs -f <service>`.
