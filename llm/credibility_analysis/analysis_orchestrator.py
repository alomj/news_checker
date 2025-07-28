from llm.credibility_analysis.batch_processor import BatchProcessor
from llm.credibility_analysis.llm_analyzer import LLMAnalyzer
from llm.credibility_analysis.result_merger import ResultMerger
from schema import SearchResponse
from utils.concurrency_limiter import ConcurrencyLimiter


class AnalyzerOrchestrator:
    def __init__(self, llm_analyzer: LLMAnalyzer):
        self.llm_analyzer = llm_analyzer
        self.limiter = ConcurrencyLimiter()

    async def process(self, search_response: SearchResponse):
        batch_processor = BatchProcessor(search_response)
        result_merger = ResultMerger(search_response)

        batches, metadata = batch_processor.process()

        tasks = [self.llm_analyzer.analyze_batch(batch) for batch in batches]
        completed_tasks = await self.limiter.execute_tasks(tasks)
        result = result_merger.merge(completed_tasks, metadata)

        return result
