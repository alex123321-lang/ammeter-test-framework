from src.pipeline.pipeline import Pipeline

from src.pipeline.steps.collector_step import CollectorStep
from src.pipeline.steps.analysis_step import AnalysisStep
from src.pipeline.steps.accuracy_step import AccuracyStep
from src.pipeline.steps.visualization_step import VisualizationStep
from src.pipeline.steps.save_step import SaveStep


def build_pipeline(collector, analyzer, visualizer, reporter, config, logger):
    """
    Builds the full execution pipeline using DI.
    """

    return Pipeline([

        # 1. Collect data
        CollectorStep(
            collector=collector,
            sampling_config=config.testing.sampling,
            logger=logger
        ),

        # 2. Calculate statistics
        AnalysisStep(
            analyzer=analyzer,
            metrics=config.analysis.statistical_metrics
        ),

        # 3. Accuracy check (logs warning)
        AccuracyStep(
            threshold=config.analysis.accuracy.threshold,
            logger=logger
        ),

        # 4. Visualization
        VisualizationStep(
            visualizer=visualizer,
            config=config.analysis.visualization,
            logger=logger
        ),

        # 5. Save results
        SaveStep(
            reporter=reporter,
            config=config.result_management,
            logger=logger
        )
    ])