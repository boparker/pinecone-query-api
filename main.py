import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pinecone import Pinecone
import uvicorn
import traceback

# Load required environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("INDEX_NAME")

if not all([pinecone_api_key, index_name]):
    raise RuntimeError("Missing Pinecone environment variables.")

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)

# Initialize FastAPI app
app = FastAPI()

# Pydantic request model
class QueryRequest(BaseModel):
    query: list  # Should be 1024-dim for your use case
    top_k: int = 5

@app.get("/")
def root():
    return {"message": "✅ Pinecone Query API is live."}

@app.post("/query")
def query_index(req: QueryRequest):
    try:
        # Attempt Pinecone query
        res = index.query(vector=req.query, top_k=req.top_k, include_metadata=True)
        return res
    except Exception as e:
        # Return full traceback for debugging
        tb = tr
