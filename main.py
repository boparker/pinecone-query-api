import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pinecone
import uvicorn

# Load environment variables safely
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
index_name = os.getenv("INDEX_NAME")

# Fail fast if any env var is missing
if not all([pinecone_api_key, pinecone_env, index_name]):
    raise RuntimeError("❌ Missing Pinecone env vars. Set PINECONE_API_KEY, PINECONE_ENV, and INDEX_NAME.")

# Init Pinecone
pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
index = pinecone.Index(index_name)

# Setup FastAPI
app = FastAPI()

# Request model
class QueryRequest(BaseModel):
    query: list  # Must be a vector list (e.g. [0.1, 0.2, 0.3])
    top_k: int = 5

@app.get("/")
def root():
    return {"message": "✅ Pinecone Query API is live."}

@app.post("/query")
def query_index(req: QueryRequest):
    try:
        res = index.query(vector=req.query, top_k=req.top_k, include_metadata=True)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

# Required for Railway or Render — binds to $PORT
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
