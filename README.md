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
  - `docker/full-stack/`: Flowise, n8n, Open WebUI, Qdrant and Ollama together, with Qdrant
    and Ollama as shared services. See `docker/full-stack/README.md`. Confirmation:
    `docker/full-stack/docker-compose.yml`.
- Every stack runs third-party images from Docker Hub or GitHub Container Registry. Own code
  here is limited to the Compose files and the two workflows.
- `docker/flowise/.env.example`, `docker/n8n/.env.example` and
  `docker/full-stack/.env.example` are templates for `.env`. Flowise, n8n and the full
  stack will not start without a password: `FLOWISE_PASSWORD` (Flowise, full stack) and
  `N8N_PASSWORD` (n8n, full stack) have no default, and `docker compose` exits with an
  error if they are unset. API keys are optional. The Open WebUI and Qdrant stacks need no
  `.env`; Open WebUI and Ollama run models locally.
- Every published port in every stack is bound to `127.0.0.1`, so the services are
  reachable only from the machine that runs them. See "Remote access" below.
- Four project briefs with setup steps and code listings: `projects/01-faq-chatbot/README.md`,
  `projects/02-rag-pdf/README.md`, `projects/03-agent-websearch/README.md`,
  `projects/04-n8n-email-ai/README.md`.
- Two GitHub Actions workflows in `.github/workflows/`:
  - `validate-compose.yml` runs `docker compose config -q` for each of the five stacks. It
    copies `.env.example` to `.env` first, so the check uses the example values. It runs
    on pull requests that touch `docker/**` or the workflow itself, and on pushes to
    `main` that do.
  - `learning-tracker.yml` regenerates `PROGRESS.md` from the contents of `projects/`. It
    runs on pushes that touch `projects/**` and can be started manually.
- `.gitignore` excludes `.env` and `.env.*` (but keeps `.env.example`), local data and
  volume directories (`data/`, `volumes/`, `qdrant_storage/`, `ollama_models/`,
  `flowise_data/`, `n8n_data/`, `open_webui_data/`, `.flowise/`, `.n8n/`), `*.log` (except
  `logs/activity.log`), temporary files, OS files and editor directories.

## Quick start

Any single stack:

```bash
git clone https://github.com/FreeAiHub/ai-lab.git
cd ai-lab/docker/flowise
cp .env.example .env       # set FLOWISE_PASSWORD (required); add OPENAI_API_KEY if wanted
docker compose up -d
# → http://localhost:3000
```

All of it at once:

```bash
cd docker/full-stack
cp .env.example .env       # set FLOWISE_PASSWORD and N8N_PASSWORD (both required)
docker compose up -d
```

Confirmed against `docker/flowise/docker-compose.yml` and
`docker/full-stack/docker-compose.yml`. The full stack expects 16GB of RAM, per the comment
at the top of that file.

The `.env.example` values are placeholders (`change-me`, `n8n-change-me`,
`flowise-change-me`). Compose accepts them, so replace them with your own passwords.

Ports, taken from the Compose files rather than guessed. All are published on `127.0.0.1`
only (for example `"127.0.0.1:3000:3000"`):

| Stack | Ports (host, loopback only) |
|---|---|
| Flowise | 3000 |
| n8n | 5678 |
| Open WebUI + Ollama | 8080, 11434 |
| Qdrant | 6333 (HTTP), 6334 (gRPC) |
| Full stack | 3000, 5678, 8080, 11434, 6333, 6334 |

### Remote access

Because the ports are bound to loopback, another machine on the network cannot connect to
them. To use a stack running on a remote host, open an SSH tunnel from your own machine, for
example:

```bash
ssh -L 3000:127.0.0.1:3000 -L 5678:127.0.0.1:5678 -L 8080:127.0.0.1:8080 user@host
```

Then browse to `http://localhost:3000` and so on. To expose a service on other interfaces,
change the left-hand `127.0.0.1` in the `ports` entry of the Compose file, and set strong
passwords first.

### Environment variables

| Variable | Used by | Default if unset |
|---|---|---|
| `FLOWISE_USERNAME` | Flowise login | `admin` |
| `FLOWISE_PASSWORD` | Flowise login | none; `docker compose` fails ("set it in .env") |
| `N8N_USER` | n8n basic auth user | `admin` |
| `N8N_PASSWORD` | n8n basic auth password | none; `docker compose` fails ("set it in .env") |
| `OPENAI_API_KEY` | Flowise, Open WebUI; also n8n in the standalone n8n stack | empty |

`docker/flowise/docker-compose.yml` reads `.env` as an optional `env_file`, so a missing
`.env` file is not an error by itself. The password must still reach Compose some other
way, for example as an exported shell variable. Without it, `docker compose` fails. The
full-stack file has no `env_file`; Compose reads `.env` in that directory for substitution.
The Flowise stack also passes any other variable in its `.env` into the container, which is
why its `.env.example` lists `ANTHROPIC_API_KEY` and `OPENROUTER_API_KEY`.

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
- No tests and no linting. The only CI is the two workflows above: `validate-compose.yml`
  checks that each Compose file parses (`docker compose config -q`), which does not start
  any container or test any service, and `learning-tracker.yml` rebuilds `PROGRESS.md`.
- `PROGRESS.md` is generated by `learning-tracker.yml`; do not edit it by hand. A project
  counts as done when its directory under `projects/` contains at least one `.py`, `.json`
  or `.js` file, so adding any such file marks it done regardless of whether the project
  works. It currently reports 0 of 4.
- No `LICENSE` file. The repository is public, so the default terms apply.
- `logs/activity.log` counts files, not work. All 133 entries since 2026-03-18 read
  "Files in repo: 21", while the sync kept running. That is why this README dates the
  content, not the last commit.
