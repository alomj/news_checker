from pydantic import BaseModel
from typing import List, Optional


class Request(BaseModel):
    headline: str


class SearchRequest(BaseModel):
    headlines: List[str]


class SearchHit(BaseModel):
    title: str | None = None
    url: str | None = None
    credibility_score: Optional[float] | None = None
    flags: Optional[dict] | None = None


class QueryResult(BaseModel):
    query: str
    results: List[SearchHit]


class HeadlineQueryResponse(BaseModel):
    headline: str
    queries: List[QueryResult]


class SearchResponse(BaseModel):
    items: List[HeadlineQueryResponse]
