from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from pinecone import Pinecone

app = FastAPI()

pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_index = os.environ.get("INDEX_NAME")

if not pinecone_api_key or not pinecone_index:
    raise RuntimeError("Missing required environment variables.")

pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index)

class QueryRequest(BaseModel):
    query: list[float]
    top_k: int = 5

@app.post("/query")
def query_index(request: QueryRequest):
    try:
        response = index.query(
            vector=request.query,
            top_k=request.top_k,
            include_metadata=True
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
