from services.search_client import SearchService
from services.openai_client import OpenAiService
from fastapi import Depends


def get_llm_engine() -> OpenAiService:
    return OpenAiService()


def get_search_engine(llm_engine: OpenAiService = Depends(get_llm_engine)) -> SearchService:
    return SearchService(llm_engine)
