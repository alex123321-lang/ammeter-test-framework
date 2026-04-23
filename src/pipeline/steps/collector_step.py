from src.pipeline.base_step import PipelineStep


class CollectorStep(PipelineStep):

    def __init__(self, collector, sampling_config, logger):
        self.collector = collector
        self.sampling_config = sampling_config
        self.logger = logger

    def process(self, result):
        cfg = result.meta["ammeter_cfg"]

        stream = self.collector.stream_measurements(
            result.ammeter_type,
            cfg,
            self.sampling_config
        )

        result.stream = stream  #  pass stream forward

        return result