from fastapi import FastAPI, status, Depends
from config import settings
from services.openai_client import OpenAiService
from llm.query_generator import QueryGenerator
from schema import SearchRequest, Request, SearchResponse
from services.search_client import SearchService
from utils.get_clients import get_search_engine, get_llm_analyzer
from llm.technical_analyzer import TechnicalAnalyzer
from llm.credibility_analysis.llm_analyzer import LLMAnalyzer

app = FastAPI(title=settings.app_title,
              description=settings.app_description
              )


@app.post('/generate-news', status_code=status.HTTP_201_CREATED, response_model=None)
async def generate_news(request: Request):
    client = OpenAiService()
    generator = QueryGenerator(client)
    query = await generator.generate(headline=request.headline)

    return query


@app.post('/search-news', status_code=status.HTTP_201_CREATED, response_model=SearchResponse)
async def search_news(request: SearchRequest,
                      search_service: SearchService = Depends(get_search_engine)):
    items = await search_service.generate(request.headlines)
    return items


@app.post('/rate-search', status_code=status.HTTP_201_CREATED, response_model=SearchResponse)
async def rate_news(search_response: SearchResponse,
                    llm_analyzer: LLMAnalyzer = Depends(get_llm_analyzer)):
    technical_analyzer = TechnicalAnalyzer(llm_analyzer)
    result = await technical_analyzer.analyze(search_response)
    return result
