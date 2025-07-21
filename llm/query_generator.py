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
                    "You are a search expert. Given a news headline, generate 3 effective "
                    "search queries to fact-check it using trustworthy sources."
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
