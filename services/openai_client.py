import httpx
from typing import List, Optional
from fastapi import status, HTTPException
from config import Settings, get_settings
from tenacity import retry, stop_after_attempt, before_log, after_log
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

logger = logging.getLogger(__name__)


class OpenAiService:
    def __init__(self, settings: Optional[Settings] = None,
                 client: Optional[httpx.AsyncClient] = None):
        if settings is None:
            try:
                settings = get_settings()
            except Exception as e:
                raise ValueError(f'Could not load OpenAI settings {e}')

        self.model = settings.model
        self.api_key = settings.openai_key
        self.base_url = settings.base_url
        self._client = client

    @retry(stop=stop_after_attempt(4), before=before_log(logger, logging.DEBUG),
           after=after_log(logger, logging.DEBUG),
           reraise=True)
    async def ask(self, messages: List[dict]) -> dict:
        header = {
            "Authorization": f'Bearer {self.api_key}',
            "Content-Type": "application/json"
        }
        json_data = {
            'model': self.model,
            'messages': messages
        }
        try:
            if self._client:
                response = await self._client.post(self.base_url, headers=header, json=json_data)
                response.raise_for_status()
                return response.json()
            else:
                async with httpx.AsyncClient() as client:
                    response = await client.post(self.base_url, headers=header, json=json_data)
                    response.raise_for_status()
                    return response.json()

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code,
                                detail=f'OpenAI API error: {e.response.text}')
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f'Failed to connect to OpenAI API: {str(e)}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f'Unexpected error: {str(e)}')
