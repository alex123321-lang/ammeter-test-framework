from src.pipeline.base_step import PipelineStep


class AccuracyStep(PipelineStep):
    def __init__(self, threshold, logger):
        self.threshold = threshold
        self.logger = logger

    def process(self, result):
        if not result.is_success:
            return result

        accuracy = result.statistics.get("accuracy")

        if self.threshold and accuracy and accuracy > self.threshold:
            self.logger.warning(
                f"{result.ammeter_type} unstable "
                f"(accuracy={accuracy:.4f}, threshold={self.threshold})"
            )

        return result