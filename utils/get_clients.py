from services.search_client import SearchService
from services.openai_client import OpenAiService
from interfaces.search_provider import SearchProvider
from services.search_providers.duckduckgo_provider import DuckDuckGoSearchProvider
from fastapi import Depends


def get_llm_engine() -> OpenAiService:
    return OpenAiService()


def get_search_provider() -> SearchProvider:
    return DuckDuckGoSearchProvider()


def get_search_engine(llm_engine: OpenAiService = Depends(get_llm_engine),
                      search_provider: SearchProvider = Depends(get_search_provider)) \
        -> SearchService:
    return SearchService(llm_engine, search_provider)
