# Qdrant — Vector Database

> The core of any RAG system. Stores embeddings, finds similar content fast.

## Start

```bash
docker compose up -d
```

Dashboard → http://localhost:6333/dashboard

## Python quickstart

```python
pip install qdrant-client openai
```

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import openai, os

oai = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = QdrantClient(url="http://localhost:6333")

# 1. Create collection
client.create_collection(
    "my_docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# 2. Embed text
text = "AI agents use tools to complete tasks automatically"
vector = oai.embeddings.create(
    model="text-embedding-3-small", input=text
).data[0].embedding

# 3. Store
client.upsert("my_docs", points=[
    PointStruct(id=1, vector=vector, payload={"text": text})
])

# 4. Search
query_vec = oai.embeddings.create(
    model="text-embedding-3-small", input="how do AI agents work?"
).data[0].embedding

results = client.search("my_docs", query_vector=query_vec, limit=3)
for r in results:
    print(f"Score: {r.score:.3f} | {r.payload['text']}")
```

## Key concepts

- **Vector** = text → numbers (1536 floats for OpenAI embeddings)
- **Distance** = COSINE (best for text), DOT, EUCLID
- **Collection** = like a table, but for vectors
- **Payload** = metadata stored with each vector (text, source, date)
