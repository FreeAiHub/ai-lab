# Open WebUI + Ollama — Local LLMs

> Run AI models locally, completely FREE. Good for learning without API costs.

## Start

```bash
docker compose up -d

# Pull a model (first time — downloads the model):
docker exec ollama ollama pull llama3.2:3b    # 2GB, fast responses
# OR for better quality:
docker exec ollama ollama pull qwen2.5:7b     # 4GB, better
# For embeddings (RAG without OpenAI):
docker exec ollama ollama pull nomic-embed-text  # 274MB
```

Open → http://localhost:8080

## Models for 8GB RAM Mac

| Model | Size | Best for |
|-------|------|----------|
| `llama3.2:3b` | 2GB | Fast testing |
| `qwen2.5:7b` | 4GB | Quality answers, coding |
| `nomic-embed-text` | 274MB | FREE RAG embeddings |
| `codellama:7b` | 4GB | Code generation |

## Free RAG embeddings

```python
import requests

resp = requests.post('http://localhost:11434/api/embeddings', json={
    'model': 'nomic-embed-text',
    'prompt': 'Your text here'
})
vector = resp.json()['embedding']  # 768 dimensions, free!
```
