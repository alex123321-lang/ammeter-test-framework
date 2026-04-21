import yaml

from .models import (
    AppConfig,
    TestingConfig,
    SamplingConfig,
    AmmeterConfig,
    AnalysisConfig,
    AccuracyConfig,
    VisualizationConfig,
    ResultManagementConfig,
    ReportingConfig,
)


class ConfigLoader:

    @staticmethod
    def load(path: str) -> AppConfig:
        with open(path, "r") as f:
            raw = yaml.safe_load(f)

        return AppConfig(
            testing=TestingConfig(
                sampling=SamplingConfig(**raw["testing"]["sampling"])
            ),

            ammeters={
                name: AmmeterConfig(**cfg)
                for name, cfg in raw["ammeters"].items()
            },

            analysis=AnalysisConfig(
                statistical_metrics=raw["analysis"]["statistical_metrics"],

                accuracy=AccuracyConfig(
                    **raw["analysis"]["accuracy"]
                ),

                visualization=VisualizationConfig(
                    **raw["analysis"]["visualization"]
                ),
            ),

            result_management=ResultManagementConfig(
                **raw["result_management"]
            ),

            reporting=ReportingConfig(
                **raw["reporting"]
            ),
        )