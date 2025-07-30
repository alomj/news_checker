import json
from typing import List

from services.openai_client import OpenAiService
from utils.parse_response import parse_response_with_credibility
from utils.reading_file import read_file

file = read_file('prompts/llm_analyzer.txt')


class LLMAnalyzer:
    def __init__(self, llm_client: OpenAiService):
        self.llm_client = llm_client

    async def analyze_batch(self, batch: List):
        batch_data = []

        for hit in batch:
            batch_data.append(hit.model_dump())

        messages = [
            {
                "role": "system",
                "content": file
            },
            {
                "role": "user",
                "content": json.dumps(batch_data)
            }
        ]

        response = await self.llm_client.ask(messages)

        return self._parse(response)

    @staticmethod
    def _parse(response: dict):
        return parse_response_with_credibility(response)
