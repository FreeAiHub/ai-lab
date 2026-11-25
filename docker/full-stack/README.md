# Full stack: Flowise + n8n + Qdrant + Ollama + Open WebUI

> Five services in one Compose file: a visual agent builder, a workflow tool, a vector
> database, a local model runtime and a chat UI.

Requires 16GB of RAM (recommended, per the comment at the top of `docker-compose.yml`).

## Start

```bash
cp .env.example .env
# Set FLOWISE_PASSWORD and N8N_PASSWORD (required), add API keys if you want hosted models
docker compose up -d
```

`FLOWISE_PASSWORD` and `N8N_PASSWORD` have no defaults. If either is unset, `docker compose`
exits with an error ("set it in .env") and starts nothing.

Open:

| Service | URL |
|---|---|
| Flowise | http://localhost:3000 |
| n8n | http://localhost:5678 |
| Open WebUI | http://localhost:8080 |
| Qdrant (HTTP) | http://localhost:6333 |
| Qdrant (gRPC) | localhost:6334 |
| Ollama API | http://localhost:11434 |

Every port is published on `127.0.0.1` only (for example `"127.0.0.1:3000:3000"`), so the
services are reachable only from the machine running the stack. To use them from another
machine, open an SSH tunnel to the host, for example:

```bash
ssh -L 3000:127.0.0.1:3000 -L 5678:127.0.0.1:5678 -L 8080:127.0.0.1:8080 user@host
```

To publish a port on other interfaces, change the `127.0.0.1` part of its mapping in
`docker-compose.yml`, and set strong passwords first.

## What it runs

| Service | Image | Port | Volume |
|---|---|---|---|
| `qdrant` | `qdrant/qdrant:latest` | 6333, 6334 | `qdrant_storage` |
| `ollama` | `ollama/ollama:latest` | 11434 | `ollama_models` |
| `flowise` | `flowiseai/flowise:latest` | 3000 | `flowise_data` |
| `n8n` | `n8nio/n8n:latest` | 5678 | `n8n_data` |
| `open-webui` | `ghcr.io/open-webui/open-webui:main` | 8080 | `open_webui_data` |

All five use `restart: unless-stopped`. Ports are bound to `127.0.0.1`. Qdrant publishes
both 6333 (HTTP) and 6334 (gRPC), as the standalone `docker/qdrant/` stack does.

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
| `FLOWISE_PASSWORD` | Flowise login | none; required, `docker compose` fails if unset |
| `N8N_USER` | n8n basic auth user | `admin` |
| `N8N_PASSWORD` | n8n basic auth password | none; required, `docker compose` fails if unset |
| `OPENAI_API_KEY` | Flowise and Open WebUI | empty |
| `ANTHROPIC_API_KEY` | Flowise | empty |
| `OPENROUTER_API_KEY` | Flowise | empty |

The two passwords are required: the Compose file uses `${VAR:?set it in .env}`, so every
`docker compose` command in this directory (including `up`, `down` and `ps`) fails while
either is unset. The values in `.env.example` (`flowise-change-me`, `n8n-change-me`) are
placeholders that Compose accepts as they are; replace them with your own passwords.

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

- **Port already in use.** Ports 3000, 5678, 6333, 6334, 8080 and 11434 are published on
  `127.0.0.1`. Stop whatever holds the port, or change the host port in the mapping in
  `docker-compose.yml` (for example `"127.0.0.1:3001:3000"`).
- **Cannot connect from another machine.** Expected: the ports are loopback-only. Use an SSH
  tunnel (see above).
- **Out of memory or the machine slows down.** The stack is sized for 16GB. Start fewer
  services, for example `docker compose up -d open-webui` starts only Open WebUI and
  Ollama.
- **Open WebUI shows no models.** The Ollama volume starts empty. Pull a model, for example
  `docker exec ollama ollama pull llama3.2`, then refresh.
- **Flowise or n8n cannot reach Qdrant or Ollama.** Use `http://qdrant:6333` and
  `http://ollama:11434`, not `localhost`, from inside those containers.
- **`docker compose` fails with "set it in .env".** `FLOWISE_PASSWORD` or `N8N_PASSWORD` is
  unset. Create `.env` from `.env.example` and set both.
- **Cannot log in.** Check the username and password in `.env`. The usernames default to
  `admin`; the passwords have no default. After changing credentials, run
  `docker compose up -d` again to recreate the containers.
- **See what is happening.** `docker compose ps` and `docker compose logs -f <service>`.
