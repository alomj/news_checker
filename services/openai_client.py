from config import open_api_setting
import httpx
from typing import List


class OpenAiService:
    def __init__(self):
        self.model = open_api_setting.model
        self.api_key = open_api_setting.openai_key
        self.base_url = open_api_setting.base_url

    async def ask(self, messages: List[dict]) -> dict:
        header = {
            "Authorization": f'Bearer {self.api_key}',
            "Content-Type": "application/json"
        }
        json_data = {
            'model': self.model,
            'messages': messages
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=header, json=json_data)
            response.raise_for_status()
            return response.json()
