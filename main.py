from fastapi import FastAPI, status, Depends
from config import settings
from llm.query_generator import QueryGenerator
from schema import SearchRequest, Request, SearchResponse
from services.search_client import SearchService
from utils.get_clients import get_search_engine, get_query_generator, \
    get_technical_analyzer
from llm.technical_analyzer import TechnicalAnalyzer

app = FastAPI(title=settings.app_title,
              description=settings.app_description
              )


@app.post('/news-checker', status_code=status.HTTP_201_CREATED, response_model=SearchResponse)
async def fake_checker(request: Request,
                       search_service: SearchService = Depends(get_search_engine),
                       query_generator: QueryGenerator = Depends(get_query_generator),
                       technical_analyzer: TechnicalAnalyzer = Depends(get_technical_analyzer)
                       ):
    query = await query_generator.generate(headline=request.headline)

    search_items = await search_service.generate(query)

    result = await technical_analyzer.analyze(search_response=search_items)

    return result


@app.post('/generate-news', status_code=status.HTTP_201_CREATED, response_model=None)
async def generate_news(request: Request,
                        query_generator: QueryGenerator = Depends(get_query_generator)):
    query = await query_generator.generate(headline=request.headline)

    return query


@app.post('/search-news', status_code=status.HTTP_201_CREATED, response_model=SearchResponse)
async def search_news(request: SearchRequest,
                      search_service: SearchService = Depends(get_search_engine)):
    items = await search_service.generate(request.headlines)
    return items


@app.post('/rate-search', status_code=status.HTTP_201_CREATED, response_model=SearchResponse)
async def rate_news(search_response: SearchResponse,
                    technical_analyzer: TechnicalAnalyzer = Depends(get_technical_analyzer)):
    result = await technical_analyzer.analyze(search_response)
    return result
