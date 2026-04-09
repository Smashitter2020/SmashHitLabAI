from fastapi import FastAPI
from pydantic import BaseModel
from assistant.rag import RAGPipeline

app = FastAPI(
    title="Smash Hit Lab Local Assistant API",
    description="Local RAG-powered API for Smash Hit modding guidance",
    version="1.0.0"
)

pipeline = RAGPipeline()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    answer, docs, meta = pipeline.answer(req.question)
    sources = [m.get("source", "unknown") for m in meta]
    return QueryResponse(answer=answer, sources=sources)


@app.get("/sources")
def list_sources():
    # Return metadata about all indexed documents
    collection = pipeline.collection
    count = collection.count()

    return {
        "documents_indexed": count,
        "embedding_model": pipeline.embed_model_name,
        "llm_model": pipeline.model_name,
    }