from llm.credibility_analysis.llm_analyzer import LLMAnalyzer
from llm.credibility_analysis.analysis_orchestrator import AnalyzerOrchestrator
from schema import SearchResponse


class TechnicalAnalyzer:
    def __init__(self, llm_analyzer: LLMAnalyzer):
        self.llm_analyzer = llm_analyzer

    async def analyze(self, search_response: SearchResponse):
        orchestrator = AnalyzerOrchestrator(
            llm_analyzer=self.llm_analyzer
        )

        return await orchestrator.process(search_response)
