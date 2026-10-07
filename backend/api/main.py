from fastapi import FastAPI

from backend.core.config import get_settings
from backend.core.models import QueryRequest, QueryResponse


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Evaluation-driven production RAG platform.",
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    return QueryResponse(
        success=True,
        query=request.query.strip(),
        answer=None,
    )
