from services.openai_client import OpenAiService
from typing import List


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
        content = response['choices'][0]['message']['content']
        lines = content.strip().split("\n")
        return [line.lstrip('123456789. ').strip() for line in lines if line.strip()]
