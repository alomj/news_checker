import httpx
from typing import List, Optional
from fastapi import status, HTTPException
from config import OpenAISettings


class OpenAiService:
    def __init__(self, settings: Optional[OpenAISettings] = None,
                 client: Optional[httpx.AsyncClient] = None):
        self.model = settings.model
        self.api_key = settings.openai_key
        self.base_url = settings.base_url
        self._client = client

    async def ask(self, messages: List[dict]) -> dict:
        header = {
            "Authorization": f'Bearer {self.api_key}',
            "Content-Type": "application/json"
        }
        json_data = {
            'model': self.model,
            'messages': messages
        }

        if self._client:
            response = await self._client.post(self.base_url, headers=header, json=json_data)
        else:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.base_url, headers=header, json=json_data)
                response.raise_for_status()

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status_code, detail="OpenAI request failed")

        return response.json()
