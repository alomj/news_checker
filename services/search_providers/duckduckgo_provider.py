from typing import List, Dict

from ddgs import DDGS
from interfaces.search_provider import SearchProvider
from config import Settings


class DuckDuckGoSearchProvider(SearchProvider):
    def search(self, query: str) -> List[Dict]:
        with DDGS() as ddgs:
            return list(ddgs.news(query, max_search=Settings().max_search_results))
