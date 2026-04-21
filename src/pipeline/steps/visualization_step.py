from src.pipeline.base_step import PipelineStep


class VisualizationStep(PipelineStep):
    def __init__(self, visualizer, viz_config):
        self.visualizer = visualizer
        self.viz_config = viz_config

    def process(self, result):
        if not result.is_success:
            return result

        self.visualizer.visualize_results(
            result.ammeter_type,
            result.measurements,
            self.viz_config
        )
        return result