# Pinecone Query API

A FastAPI service to query a Pinecone vector index. Deployable to Railway.

## 🚀 Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## 🧪 Example POST to /query

```json
{
  "query": [0.1, 0.2, 0.3],
  "top_k": 5
}
```

## 📦 Env Vars Required

- `PINECONE_API_KEY`
- `PINECONE_ENV`
- `INDEX_NAME`
- `PORT` (injected by Railway)
