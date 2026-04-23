from src.pipeline.base_step import PipelineStep


class AnalysisStep(PipelineStep):

    def __init__(self, analyzer, metrics):
        self.analyzer = analyzer
        self.metrics = metrics

    def process(self, result):
        self.analyzer.reset()

        measurements = []

        for m in result.stream:
            self.analyzer.update(m)
            measurements.append(m)

        result.measurements = measurements
        result.statistics = self.analyzer.finalize(self.metrics)

        return result