import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pinecone
import uvicorn

# Load environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
index_name = os.getenv("INDEX_NAME")

if not all([pinecone_api_key, pinecone_env, index_name]):
    raise RuntimeError("Missing Pinecone environment variables.")

pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
index = pinecone.Index(index_name)

app = FastAPI()

class QueryRequest(BaseModel):
    query: list
    top_k: int = 5

@app.get("/")
def root():
    return {"message": "✅ Pinecone Query API is live."}

@app.post("/query")
def query_index(req: QueryRequest):
    try:
        result = index.query(vector=req.query, top_k=req.top_k, include_metadata=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
