from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import pinecone
import uvicorn

# Load environment variables
load_dotenv()

# Initialize Pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)

# Get index name from environment variable
index_name = os.getenv("PINECONE_INDEX_NAME")
index = pinecone.Index(index_name)

# Define request model
class QueryRequest(BaseModel):
    query: list
    top_k: int = 5
    namespace: str = ""  # ✅ added namespace support

# Initialize FastAPI app
app = FastAPI()

# Define query endpoint
@app.post("/query")
def query_index(req: QueryRequest):
    try:
        res = index.query(
            vector=req.query,
            top_k=req.top_k,
            include_metadata=True,
            namespace=req.namespace  # ✅ now using passed-in namespace
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
