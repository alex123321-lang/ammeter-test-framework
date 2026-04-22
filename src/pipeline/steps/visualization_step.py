from src.pipeline.base_step import PipelineStep


class VisualizationStep(PipelineStep):
    def __init__(self, visualizer, config, logger):
        self.visualizer = visualizer
        self.config = config
        self.logger = logger

    def process(self, result):
        if not result.is_success:
            return result

        self.visualizer.visualize_results(
            result.ammeter_type,
            result.measurements,
            self.config
        )
        return result