from schema import SearchResponse
from typing import List


class ResultMerger:
    def __init__(self, original_response: SearchResponse):
        self.response = original_response

    def merge(self, batches: List, metadata: List):
        all_results = []
        for b in batches:
            if b is not None:
                all_results.extend(b)

        for current_score, current_metadata in zip(all_results, metadata):
            if not isinstance(current_score, dict):
                current_score = {
                    'credibility_score': 50,
                    'flags': {'sensational_tone': False, 'unsupported_claims': False}
                }

            item_idx = current_metadata['item_index']
            query_idx = current_metadata['query_index']
            result_idx = current_metadata['result_index']

            target_hit = self.response.items[item_idx].queries[query_idx].results[result_idx]

            target_hit.credibility_score = current_score['credibility_score']
            target_hit.flags = current_score['flags']

        return self._sort_response_by_score()

    def _sort_response_by_score(self):
        for item in self.response.items:
            for query in item.queries:
                query.results.sort(key=lambda r: r.credibility_score if r.credibility_score else 0, reverse=True)

        return self.response
