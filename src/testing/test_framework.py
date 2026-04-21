from src.config.config_loader import ConfigLoader
from src.utils.logger import setup_logger

from src.collector import AmmeterCollector
from src.analyzer import AmmeterAnalyzer
from src.visualizer import AmmeterVisualizer
from src.reporter import AmmeterReporter
from src.comparator import AmmeterComparator


class AmmeterTestFramework:
    def __init__(self, config_path="config/config.yaml"):
        self.config = ConfigLoader.load(config_path)
        self.logger = setup_logger("AmmeterTestFramework")

        self.collector = AmmeterCollector(self.logger)
        self.analyzer = AmmeterAnalyzer(self.logger)
        self.visualizer = AmmeterVisualizer(self.logger)
        self.reporter = AmmeterReporter(self.logger)
        self.comparator = AmmeterComparator(self.logger)

    def run_tests(self):
        results = {}

        for ammeter_type, cfg in self.config.ammeters.items():

            if not cfg.enabled:
                continue

            try:
                self.logger.info(f"Starting test for {ammeter_type} ammeter")

                measurements = self.collector.collect_measurements(
                    ammeter_type,
                    cfg,
                    self.config.testing.sampling
                )

                stats = self.analyzer.calculate_statistics(
                    measurements,
                    self.config.analysis.statistical_metrics
                )

                accuracy = stats.get("accuracy")
                threshold = self.config.analysis.accuracy.threshold

                if threshold and accuracy and accuracy > threshold:
                    self.logger.warning(
                        f"{ammeter_type} unstable (accuracy={accuracy:.4f}, threshold={threshold})"
                    )

                self.visualizer.visualize_results(
                    ammeter_type,
                    measurements,
                    self.config.analysis.visualization
                )

                self.reporter.save_results(
                    ammeter_type,
                    measurements,
                    stats,
                    self.config.result_management
                )

                self.logger.info(f"Test completed for {ammeter_type} ammeter")

                results[ammeter_type] = {
                    "measurements": measurements,
                    "statistics": stats
                }

            except Exception as e:
                self.logger.error(f"Test failed for {ammeter_type} ammeter: {e}")
                results[ammeter_type] = {"error": str(e)}

        self.comparator.comparative_analysis(results)
        self.reporter.generate_report(results, self.config)

        return results