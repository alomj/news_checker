from services.search_client import SearchService
from services.openai_client import OpenAiService
from llm.query_generator import QueryGenerator
from interfaces.search_provider import SearchProvider
from llm.credibility_analysis.llm_analyzer import LLMAnalyzer
from services.search_providers.duckduckgo_provider import DuckDuckGoSearchProvider
from llm.technical_analyzer import TechnicalAnalyzer
from fastapi import Depends


def get_llm_engine() -> OpenAiService:
    return OpenAiService()


def get_search_provider() -> SearchProvider:
    return DuckDuckGoSearchProvider()


def get_search_engine(llm_engine: OpenAiService = Depends(get_llm_engine),
                      search_provider: SearchProvider = Depends(get_search_provider)) \
        -> SearchService:
    return SearchService(llm_engine, search_provider)


def get_llm_analyzer(llm_engine: OpenAiService = Depends(get_llm_engine)) -> LLMAnalyzer:
    return LLMAnalyzer(llm_engine)


def get_query_generator(llm_engine: OpenAiService = Depends(get_llm_engine)) -> QueryGenerator:
    return QueryGenerator(llm_engine)


def get_technical_analyzer(llm_analyzer: LLMAnalyzer =
                           Depends(get_llm_analyzer)) -> TechnicalAnalyzer:
    return TechnicalAnalyzer(llm_analyzer)
