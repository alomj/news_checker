import pytest
from unittest.mock import Mock, AsyncMock
import json

from llm.credibility_analysis.llm_analyzer import LLMAnalyzer

from schema import SearchHit


class TestLLMAnalyzer:
    @pytest.fixture
    def mock_llm_client(self):
        return Mock()

    @pytest.fixture
    def llm_analyzer(self, mock_llm_client):
        return LLMAnalyzer(mock_llm_client)

    @pytest.fixture
    def sample_batch(self):
        hit1 = SearchHit(title="Title 1", url="https://example1.com")
        hit2 = SearchHit(title="Title 2", url="https://example2.com")
        return [hit1, hit2]

    async def test_analyze_batch_success(self, llm_analyzer, mock_llm_client, sample_batch):
        mock_response = {
            'choices': [{
                'message': {
                    'content': json.dumps([
                        {"credibility_score": 85, "flags": {"sensational_tone": False,
                                                            "unsupported_claims": True}},
                        {"credibility_score": 60, "flags": {"sensational_tone": True,
                                                            "unsupported_claims": False}}
                    ])
                }
            }]
        }
        mock_llm_client.ask = AsyncMock(return_value=mock_response)

        result = await llm_analyzer.analyze_batch(sample_batch)

        assert len(result) == 2
        assert result[0]["credibility_score"] == 85
        assert result[0]["flags"]["sensational_tone"] is False
        assert result[1]["credibility_score"] == 60
        assert result[1]["flags"]["sensational_tone"] is True

    async def test_analyze_batch_empty_content(self, llm_analyzer, mock_llm_client, sample_batch):
        mock_response = {
            'choices': [{'message': {'content': ''}}]
        }
        mock_llm_client.ask = AsyncMock(return_value=mock_response)

        with pytest.raises(ValueError, match="Empty content from OpenAI"):
            await llm_analyzer.analyze_batch(sample_batch)
