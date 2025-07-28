import pytest
from unittest.mock import Mock, AsyncMock

from llm.query_generator import QueryGenerator


class TestQueryGenerator:
    @pytest.fixture
    def mock_llm_client(self):
        return Mock()

    @pytest.fixture
    def query_generator(self, mock_llm_client):
        return QueryGenerator(mock_llm_client)

    async def test_generate_success(self, query_generator, mock_llm_client):
        mock_response = {
            'choices': [{'message': {'content': 'Query one\n Query two\n Query three'}}]
        }
        mock_llm_client.ask = AsyncMock(return_value=mock_response)

        result = await query_generator.generate("Test headline")

        assert len(result) == 3
        assert result[0] == "Query one"
        assert result[1] == "Query two"
        assert result[2] == "Query three"

    async def test_generate_empty_choices_array(self, query_generator, mock_llm_client):
        mock_response = {'choices': []}
        mock_llm_client.ask = AsyncMock(return_value=mock_response)

        with pytest.raises(ValueError, match="Empty  array in OpenAI response"):
            await query_generator.generate("Test headline")
