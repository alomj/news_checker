import pytest

from llm.credibility_analysis.result_merger import ResultMerger

from schema import SearchResponse, HeadlineQueryResponse, QueryResult, SearchHit


class TestResultMerger:
    @pytest.fixture
    def sample_search_response(self):
        hit1 = SearchHit(title="Title 1", url="https://example1.com")
        hit2 = SearchHit(title="Title 2", url="https://example2.com")

        query1 = QueryResult(query="Query 1", results=[hit1, hit2])
        headline_response = HeadlineQueryResponse(headline="Test headline", queries=[query1])

        return SearchResponse(items=[headline_response])

    def test_merge_success(self, sample_search_response):
        merger = ResultMerger(sample_search_response)
        batches = [
            [
                {"credibility_score": 85, "flags": {"sensational_tone": False,
                                                    "unsupported_claims": True}},
                {"credibility_score": 60, "flags": {"sensational_tone": True,
                                                    "unsupported_claims": False}}
            ]
        ]
        metadata = [
            {'item_index': 0, 'query_index': 0, 'result_index': 0, 'headline': 'Test',
             'query_text': 'Query 1'},
            {'item_index': 0, 'query_index': 0, 'result_index': 1, 'headline': 'Test',
             'query_text': 'Query 1'}
        ]

        result = merger.merge(batches, metadata)

        assert result.items[0].queries[0].results[0].credibility_score == 85
        assert result.items[0].queries[0].results[0].flags["sensational_tone"] is False
        assert result.items[0].queries[0].results[1].credibility_score == 60
        assert result.items[0].queries[0].results[1].flags["sensational_tone"] is True

    def test_merge_with_none_batch(self, sample_search_response):
        merger = ResultMerger(sample_search_response)
        batches = [None]
        metadata = []

        result = merger.merge(batches, metadata)

        assert len(result.items) == 1
