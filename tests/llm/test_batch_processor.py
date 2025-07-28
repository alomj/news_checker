import pytest

from llm.credibility_analysis.batch_processor import BatchProcessor

from schema import SearchResponse, HeadlineQueryResponse, QueryResult, SearchHit


class TestBatchProcessor:
    @pytest.fixture
    def sample_search_response(self):
        hit1 = SearchHit(title="Title 1", url="https://example1.com")
        hit2 = SearchHit(title="Title 2", url="https://example2.com")
        hit3 = SearchHit(title="Title 3", url="https://example3.com")

        query1 = QueryResult(query="Query 1", results=[hit1, hit2])
        query2 = QueryResult(query="Query 2", results=[hit3])

        headline_response = HeadlineQueryResponse(headline="Test headline",
                                                  queries=[query1, query2])

        return SearchResponse(items=[headline_response])

    def test_extract_all_hits_with_metadata(self, sample_search_response):
        processor = BatchProcessor(sample_search_response)

        metadata, all_hits = processor.extract_all_hits_with_metadata()

        assert len(metadata) == 3
        assert len(all_hits) == 3

        assert metadata[0]['item_index'] == 0
        assert metadata[0]['query_index'] == 0
        assert metadata[0]['result_index'] == 0
        assert metadata[0]['headline'] == "Test headline"
        assert metadata[0]['query_text'] == "Query 1"

        assert metadata[2]['query_index'] == 1
        assert metadata[2]['result_index'] == 0

    def test_process_empty_search_response(self):
        empty_response = SearchResponse(items=[])
        processor = BatchProcessor(empty_response)

        batches, metadata = processor.process()

        assert len(batches) == 0
        assert len(metadata) == 0
