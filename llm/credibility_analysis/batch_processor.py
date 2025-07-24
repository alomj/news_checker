from schema import SearchResponse

class BatchProcessor:
    def __init__(self, search_response: SearchResponse):
        self.search_response = search_response

    def extract_all_hits_with_metadata(self):
        metadata = {}
        all_hits = []

        for item_index, item in enumerate(self.search_response.items):
            for query_index, query in enumerate(item.queries):
                for result_index, hit in enumerate(query.results):
                    all_hits.append(hit)

                    hit_id = f'{len(all_hits)}_{hit.url}'

                    metadata[hit_id] = {
                        'item_index': item_index,
                        'query_index': query_index,
                        'result_index': result_index,
                        'headline': item.headline,
                        'query_text': query.query
                    }

        return metadata, all_hits

    @staticmethod
    def split_into_batches(all_hits, batch_size=5):
        batches = []

        for i in range(0, len(all_hits), batch_size):
            batch = all_hits[i:i+batch_size]
            batches.append(batch)

        return batches

    def process(self):
        metadata, all_hits = self.extract_all_hits_with_metadata()

        batches = self.split_into_batches(all_hits)

        return batches, metadata

