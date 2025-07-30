from typing import List

from services.openai_client import OpenAiService
from utils.parse_response import parse_response
from utils.reading_file import read_file

file = read_file('prompts/query_generator.txt')


class QueryGenerator:
    def __init__(self, llm_client: OpenAiService):
        self.llm = llm_client

    async def generate(self, headline: str) -> List[str]:
        messages = [
            {
                "role": "system",
                "content": file
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
