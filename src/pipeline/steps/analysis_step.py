from src.pipeline.base_step import PipelineStep


class AnalysisStep(PipelineStep):
    def __init__(self, analyzer, metrics):
        self.analyzer = analyzer
        self.metrics = metrics

    def process(self, result):
        stats = self.analyzer.calculate_statistics(
            result.measurements,
            self.metrics
        )
        result.statistics = stats
        return result