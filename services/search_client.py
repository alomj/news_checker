import asyncio
from llm.query_generator import QueryGenerator
from services.openai_client import OpenAiService
from typing import List
from schema import HeadlineQueryResponse, QueryResult, SearchHit, SearchResponse
from utils.cleaning_queries import sanitize_query
from utils.search_news import search_news


class SearchService:
    def __init__(self, llm_engine: OpenAiService):
        self.query_generator = QueryGenerator(llm_engine)

    async def generate(self, headlines: List[str]):
        result = {}

        for headline in headlines:
            queries = await self.query_generator.generate(headline)
            search_results = []
            queries = [sanitize_query(q) for q in queries]
            for query in queries:

                res = await asyncio.to_thread(search_news, query)
                search_hit = []
                for hit in res:
                    search_h = SearchHit(title=hit.get('title'),
                                         url=hit.get('url'))

                    search_hit.append(search_h)
                search_results.append(QueryResult(query=query, results=search_hit))

            result[headline] = search_results

        items = []

        for headline, queries_response in result.items():
            headline_response = HeadlineQueryResponse(headline=headline,
                                                      queries=queries_response)

            items.append(headline_response)
        return SearchResponse(items=items)
