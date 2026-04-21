from src.pipeline.pipeline import Pipeline
from src.pipeline.steps.accuracy_step import AccuracyStep
from src.pipeline.steps.analysis_step import AnalysisStep
from src.pipeline.steps.collector_step import CollectorStep
from src.pipeline.steps.save_step import SaveStep
from src.pipeline.steps.visualization_step import VisualizationStep
from src.config.config_loader import ConfigLoader
from src.utils.logger import setup_logger

from src.collector import AmmeterCollector
from src.analyzer import AmmeterAnalyzer
from src.visualizer import AmmeterVisualizer
from src.reporter import AmmeterReporter
from src.comparator import AmmeterComparator
from src.models.test_result import TestResult


class AmmeterTestFramework:
    def __init__(self, config_path="config/config.yaml"):
        self.config = ConfigLoader.load(config_path)
        self.logger = setup_logger("AmmeterTestFramework")

        self.collector = AmmeterCollector(self.logger)
        self.analyzer = AmmeterAnalyzer(self.logger)
        self.visualizer = AmmeterVisualizer(self.logger)
        self.reporter = AmmeterReporter(self.logger)
        self.comparator = AmmeterComparator(self.logger)
        self.pipeline = Pipeline([
            CollectorStep(self.collector, self.config.testing.sampling, self.logger),
            AnalysisStep(self.analyzer, self.config.analysis.statistical_metrics),
            AccuracyStep(self.config.analysis.accuracy.threshold, self.logger),
            VisualizationStep(self.visualizer, self.config.analysis.visualization),
            SaveStep(self.reporter, self.config.result_management),
])

    def run_tests(self):
        results = {}

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
                results[ammeter_type] = result

                self.logger.info(f"Test completed for {ammeter_type} ammeter")

            except Exception as e:
                self.logger.error(f"Test failed for {ammeter_type} ammeter: {e}")

                results[ammeter_type] = TestResult(
                    ammeter_type=ammeter_type,
                    measurements=[],
                    statistics={},
                    error=str(e)
                )

        # 4. Comparative analysis
        self.comparator.comparative_analysis(results)

        # 5. Report
        self.reporter.generate_report(results, self.config)

        return results