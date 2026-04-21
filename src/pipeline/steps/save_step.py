from src.pipeline.base_step import PipelineStep


class SaveStep(PipelineStep):
    def __init__(self, reporter, config):
        self.reporter = reporter
        self.config = config

    def process(self, result):
        if not result.is_success:
            return result

        self.reporter.save_results(
            result.ammeter_type,
            result.measurements,
            result.statistics,
            self.config
        )
        return result