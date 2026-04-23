from src.models.test_session import TestSession
from src.models.test_result import TestResult
from src.utils.error_classifier import classify_error


class AmmeterTestFramework:

    def __init__(
        self,
        config,
        collector,
        analyzer,
        visualizer,
        reporter,
        comparator,
        pipeline,
        logger
    ):
        self.config = config
        self.collector = collector
        self.analyzer = analyzer
        self.visualizer = visualizer
        self.reporter = reporter
        self.comparator = comparator
        self.pipeline = pipeline
        self.logger = logger

    def run_tests(self):
        session = TestSession(self.config)


        for ammeter_type, cfg in self.config.ammeters.items():

            if not cfg.enabled:
                continue

            try:
                self.logger.info(f"Starting test for {ammeter_type} ammeter")

                # 1. Create empty TestResult (NO measurements yet)
                result = TestResult(
                    ammeter_type=ammeter_type,
                    measurements=[],
                    statistics={},
                    error=None,
                    meta={
                        "ammeter_cfg": cfg,
                        "sampling": self.config.testing.sampling
                    }
                )

                # 2. Run full pipeline (collector INCLUDED inside pipeline)
                result = self.pipeline.run(result)

                # 3. Store result
                session.add_result(result)

                self.logger.info(
                    f"Test completed for {ammeter_type} ammeter (success={result.is_success})"
                )

            except Exception as e:
                error_type = classify_error(e)

                self.logger.error(
                    f"{ammeter_type} failed [{error_type}]: {e}"
                )

                session.add_result(
                    TestResult(
                        ammeter_type=ammeter_type,
                        measurements=[],
                        statistics={},
                        error=str(e),
                        error_type=error_type
                    )
                )

        # 4. Comparative analysis
        self.comparator.comparative_analysis(session)

        # 5. Report
        self.reporter.generate_report(session)

        return session