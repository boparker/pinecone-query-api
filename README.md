# Pinecone Query API

A FastAPI service to query a Pinecone index. Deployable on Railway.

## Deploy on Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## Environment Variables

- `PINECONE_API_KEY`
- `PINECONE_ENV`
- `INDEX_NAME`
- `PORT` (automatically injected by Railway)

## Example `/query` Payload

```json
{
  "query": [0.1, 0.2, 0.3],
  "top_k": 3
}
