from dataclasses import dataclass
from typing import Dict, List


# ---------- Sampling ----------
@dataclass
class SamplingConfig:
    measurements_count: int
    sampling_frequency_hz: int
    timeout_seconds: int


# ---------- Testing ----------
@dataclass
class TestingConfig:
    sampling: SamplingConfig


# ---------- Ammeter ----------
@dataclass
class AmmeterConfig:
    port: int
    command: str
    enabled: bool


# ---------- Analysis ----------
@dataclass
class AccuracyConfig:
    enable_comparison: bool
    metric: str
    threshold: float


@dataclass
class VisualizationConfig:
    enabled: bool
    save_plots: bool
    plot_dir: str
    plot_types: List[str]


@dataclass
class AnalysisConfig:
    statistical_metrics: List[str]
    accuracy: AccuracyConfig
    visualization: VisualizationConfig


# ---------- Results ----------
@dataclass
class ResultManagementConfig:
    save_results: bool
    results_dir: str


# ---------- Reporting ----------
@dataclass
class ReportingConfig:
    generate_report: bool
    report_dir: str


# ---------- Root ----------
@dataclass
class AppConfig:
    testing: TestingConfig
    ammeters: Dict[str, AmmeterConfig]
    analysis: AnalysisConfig
    result_management: ResultManagementConfig
    reporting: ReportingConfig

