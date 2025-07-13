import os
import warnings
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")
load_dotenv()

app = FastAPI()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("INDEX_NAME")

pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)
model = SentenceTransformer("intfloat/multilingual-e5-large")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/query")
async def query_index(req: QueryRequest):
    query_embedding = model.encode(req.query.strip(), normalize_embeddings=True).tolist()
    all_results = []
    
    # Search across all namespaces
    namespaces = pc.describe_index(index_name).namespaces
    for ns in namespaces:
        response = index.query(
            vector=query_embedding,
            top_k=req.top_k,
            include_metadata=True,
            namespace=ns
        )
        for match in response.matches:
            all_results.append({
                "namespace": ns,
                "score": match.score,
                "text": match.metadata.get("text", "No text found")
            })

    sorted_results = sorted(all_results, key=lambda x: x["score"], reverse=True)
    return {"query": req.query, "results": sorted_results}
