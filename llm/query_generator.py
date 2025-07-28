from services.openai_client import OpenAiService
from typing import List
from utils.parse_response import parse_response


class QueryGenerator:
    def __init__(self, llm_client: OpenAiService):
        self.llm = llm_client

    async def generate(self, headline: str) -> List[str]:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a search expert. Given a news headline,"
                    " generate 3  search queries"
                    " to fact-check it it using multiple trustworthy and independent sources."
                    " Use quotation marks for exact phrases and focus on different "
                    "verification angles. "
                    "DO NOT limit searches to specific websites "
                    "- LET the search engine find the most relevant "
                    "sources."
                    " The output should be 3 plain search engine queries, "
                    "ready to use in DuckDuckGo or Google."
                )
            },
            {
                "role": "user",
                "content": headline
            }
        ]

        response = await self.llm.ask(messages)
        return self._parse(response)

    @staticmethod
    def _parse(response: dict) -> List[str]:
        return parse_response(response)
