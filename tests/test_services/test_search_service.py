import pytest
from unittest.mock import Mock, AsyncMock
from services.search_client import SearchService


class TestSearchService:
    @pytest.fixture
    def mock_llm_engine(self):
        return Mock()

    @pytest.fixture
    def mock_search_provider(self):
        provider = Mock()
        provider.search = Mock(return_value=[
            {"title": "Test Article", "url": "https://example.com"}
        ])
        return provider

    @pytest.fixture
    def search_service(self, mock_llm_engine, mock_search_provider):
        return SearchService(mock_llm_engine, mock_search_provider)

    async def test_generate_success(self, search_service, mock_llm_engine):
        mock_llm_engine.ask = AsyncMock(return_value={
            'choices': [{'message': {'content': 'Query one\n Query two'}}]
        })

        result = await search_service.generate(["Test headline"])

        assert len(result.items) == 1
        assert result.items[0].headline == "Test headline"
        assert len(result.items[0].queries) == 2

    async def test_generate_search_provider_failure(self, search_service,
                                                    mock_llm_engine, mock_search_provider):
        mock_llm_engine.ask = AsyncMock(return_value={
            'choices': [{'message': {'content': 'Query one'}}]
        })
        mock_search_provider.search.side_effect = Exception("Search failed")

        with pytest.raises(Exception, match="Search failed"):
            await search_service.generate(["Test headline"])
