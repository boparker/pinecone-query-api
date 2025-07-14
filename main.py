import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pinecone import Pinecone

# Load environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("INDEX_NAME")

if not all([pinecone_api_key, index_name]):
    raise RuntimeError("Missing Pinecone environment variables.")

# Create Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

# Get index
index = pc.Index(index_name)

# Setup FastAPI
app = FastAPI()

# Request model
class QueryRequest(BaseModel):
    query: list
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
