from src.config.config_loader import ConfigLoader
from src.testing.test_framework import AmmeterTestFramework

from src.collector import AmmeterCollector
from src.analyzer import AmmeterAnalyzer
from src.visualizer import AmmeterVisualizer
from src.reporter import AmmeterReporter
from src.comparator import AmmeterComparator
from src.pipeline.build_pipeline import build_pipeline
from src.utils.logger import setup_logger


def main():
    # 1. Load config 
    config = ConfigLoader.load("config/config.yaml")

    logger = setup_logger("AmmeterTestFramework")

    # 2. Create dependencies
    collector = AmmeterCollector(logger)
    analyzer = AmmeterAnalyzer(logger)
    visualizer = AmmeterVisualizer(logger)
    reporter = AmmeterReporter(logger)
    comparator = AmmeterComparator(logger)

    pipeline = build_pipeline(
        collector=collector,
        analyzer=analyzer,
        visualizer=visualizer,
        reporter=reporter,
        config=config,
        logger=logger
    )

    # 3. Inject everything
    framework = AmmeterTestFramework(
        config=config,
        collector=collector,
        analyzer=analyzer,
        visualizer=visualizer,
        reporter=reporter,
        comparator=comparator,
        pipeline=pipeline,
        logger=logger
    )

    # 4. Run
    framework.run_tests()


if __name__ == "__main__":
    main()