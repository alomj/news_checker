from services.openai_client import OpenAiService
from utils.parse_response import parse_response_with_credibility
from typing import List
import json


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
                "content": "Analyze credibility of the news articles provided by user. "
                           "Return JSON array with same number of elements in same order: "
                           '[{"credibility_score": 0-100, "flags": '
                           '{"sensational_tone": bool, "unsupported_claims": bool}}]'

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
