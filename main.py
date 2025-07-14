import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pinecone import Pinecone
import uvicorn
import traceback

# Load env vars
pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("INDEX_NAME")

if not all([pinecone_api_key, index_name]):
    raise RuntimeError("Missing Pinecone environment variables.")

# Pinecone client
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)

# FastAPI app
app = FastAPI()

# Request model
class QueryRequest(BaseModel):
    query: list
    top_k: int = 5

# Catch all exceptions globally and show trace
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "traceback": traceback.format_exc()
        }
    )

@app.get("/")
def root():
    return {"message": "✅ Pinecone Query API is live."}

@app.post("/query")
def query_index(req: QueryRequest):
    res = index.query(
        vector=req.query,
        top_k=req.top_k,
        include_metadata=True
    )
    return res

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
