import pytest
from httpx import AsyncClient, MockTransport
import httpx
from fastapi import status, HTTPException
from services.openai_client import OpenAiService
from pydantic_settings import BaseSettings


class FakeSettings(BaseSettings):
    openai_key: str = "fake-key"
    model: str = "fake-model"
    base_url: str = "http://fake-url"


class TestOpenAiService:
    async def test_client_get_success(self):
        settings = FakeSettings()

        def mock_send(request):
            return httpx.Response(status_code=status.HTTP_200_OK,
                                  json={"choices": [{"message": {"content": 'Fake News'}}]})

        transport = MockTransport(mock_send)

        async with AsyncClient(transport=transport) as client:
            service = OpenAiService(client=client, settings=settings)

            messages = [{'role': 'user', 'content': 'Test'}]

            result = await service.ask(messages)

            assert result == {"choices": [{"message": {"content": 'Fake News'}}]}

    async def test_client_get_fail(self):
        settings = FakeSettings()

        def mock_send(request):
            return httpx.Response(status_code=status.HTTP_401_UNAUTHORIZED)

        transport = MockTransport(mock_send)

        async with AsyncClient(transport=transport) as client:
            service = OpenAiService(client=client, settings=settings)

            messages = [{'role': 'user', 'content': 'Test'}]

            with pytest.raises(HTTPException) as exc_info:
                await service.ask(messages)

                assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
