from src.pipeline.base_step import PipelineStep


class CollectorStep(PipelineStep):

    def __init__(self, collector, sampling_config, logger):
        self.collector = collector
        self.sampling_config = sampling_config
        self.logger = logger

    def process(self, result):
        self.logger.info(
            f"Collecting {self.sampling_config.measurements_count} "
            f"measurements from {result.ammeter_type} at "
            f"{self.sampling_config.sampling_frequency_hz}Hz"
        )

        # cfg for current ammeter comes from result context OR injected mapping
        cfg = result.meta["ammeter_cfg"]

        measurements = self.collector.collect_measurements(
            result.ammeter_type,
            cfg,
            self.sampling_config
        )

        result.measurements = measurements

        self.logger.info(
            f"Collected {len(measurements)} measurements from {result.ammeter_type}"
        )

        return result