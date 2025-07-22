import asyncio
from llm.query_generator import QueryGenerator
from services.openai_client import OpenAiService
from typing import List, Dict
from schema import HeadlineQueryResponse, QueryResult, SearchHit, SearchResponse
from utils.cleaning_queries import sanitize_query
from utils.search_news import search_news


class SearchService:
    def __init__(self, llm_engine: OpenAiService):
        self.query_generator = QueryGenerator(llm_engine)
        self.search_news = search_news

    async def _generate_queries_for_headlines(self, headlines: List[str]):
        result = {}
        for headline in headlines:
            queries = await self.query_generator.generate(headline)
            sanitized_query = [sanitize_query(q) for q in queries]

            result[headline] = sanitized_query

        return result

    async def _execute_searches_for_queries(self, queries_by_headline: Dict[str, List[str]]):
        results = {}
        for headline, queries in queries_by_headline.items():
            results[headline] = []
            tasks = [asyncio.to_thread(self.search_news, q) for q in queries]
            search_res = await asyncio.gather(*tasks)

            for query, hits in zip(queries, search_res):
                search_hit = []
                for hit in hits:
                    title = hit.get('title')
                    url = hit.get('url')
                    if not url:
                        continue
                    search_h = SearchHit(title=title,url=url)
                    search_hit.append(search_h)
                results[headline].append(QueryResult(query=query, results= search_hit))

        return results

    @staticmethod
    async def _build_response(headlines_query: Dict[str, List[QueryResult]]):
        items = []
        for headline in headlines_query:
            headline_query_response = HeadlineQueryResponse(headline=headline,
                                  queries=headlines_query[headline])
            items.append(headline_query_response)

        return SearchResponse(items=items)

    async def generate(self, headlines: List[str]):
        queries_by_headline = await self._generate_queries_for_headlines(headlines)
        results = await self._execute_searches_for_queries(queries_by_headline)
        response = await self._build_response(results)

        return response
