from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User question",
    )


class QueryResponse(BaseModel):
    success: bool
    query: str
    answer: str | None = None
    error: str | None = None
