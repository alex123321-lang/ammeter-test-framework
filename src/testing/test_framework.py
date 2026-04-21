import time
import socket
from typing import Dict, List, Any
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from ..utils.config import load_config
from ..utils.logger import setup_logger


class AmmeterTestFramework:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = load_config(config_path)
        self.logger = setup_logger("AmmeterTestFramework")
        self.results = {}

    def request_measurement(self, port: int, command: bytes, timeout: int = 2) -> float:
        """
        Request a single measurement from an ammeter

        Args:
            port: Ammeter port
            command: Command to send
            timeout: Socket timeout in seconds

        Returns:
            Measured current value or None if failed
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect(('localhost', port))
                s.sendall(command)
                data = s.recv(1024)
                if data:
                    current = float(data.decode('utf-8'))
                    return current
                else:
                    self.logger.warning(f"No data received from port {port}")
                    return None
        except socket.timeout:
            self.logger.error(f"Timeout connecting to port {port}")
            return None
        except Exception as e:
            self.logger.error(f"Error requesting measurement from port {port}: {e}")
            return None

    def collect_measurements(self, ammeter_type: str) -> List[float]:
        """
        Collect multiple measurements from a specific ammeter

        Args:
            ammeter_type: Type of ammeter (greenlee, entes, circutor)

        Returns:
            List of measurements
        """
        ammeter_config = self.config['ammeters'].get(ammeter_type)
        if not ammeter_config or not ammeter_config.get('enabled', True):
            self.logger.warning(f"Ammeter {ammeter_type} not configured or disabled")
            return []

        port = ammeter_config['port']
        command = ammeter_config['command'].encode('utf-8')

        sampling_config = self.config['testing']['sampling']
        num_measurements = sampling_config['measurements_count']
        frequency = sampling_config['sampling_frequency_hz']
        timeout = sampling_config.get('timeout_seconds', 2)

        measurements = []
        interval = 1.0 / frequency if frequency > 0 else 0.1

        self.logger.info(f"Collecting {num_measurements} measurements from {ammeter_type} at {frequency}Hz")

        for i in range(num_measurements):
            start_time = time.time()

            measurement = self.request_measurement(port, command, timeout)
            if measurement is not None:
                measurements.append(measurement)
                self.logger.debug(f"[{ i +1}/{num_measurements}] {ammeter_type}: {measurement:.4f}A")

            # Maintain sampling frequency
            elapsed = time.time() - start_time
            sleep_time = max(0, interval - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)

        self.logger.info(f"Collected {len(measurements)} measurements from {ammeter_type}")
        return measurements

    def calculate_accuracy(self, measurements: List[float]) -> float:
        if not measurements:
            return float('inf')

        data = np.array(measurements, dtype=float)

        mean = float(np.mean(data))
        std = float(np.std(data))

        return std / mean if mean != 0 else float('inf')

    def calculate_statistics(self, measurements: List[float]) -> Dict[str, float]:
        """
        Calculate statistical metrics for measurements

        Args:
            measurements: List of measurement values

        Returns:
            Dictionary of statistical metrics
        """

        if not measurements:
            return {}

        stats = {}
        metrics = self.config['analysis']['statistical_metrics']

        data = np.array(measurements)

        if 'mean' in metrics:
            stats['mean'] = float(np.mean(data))
        if 'median' in metrics:
            stats['median'] = float(np.median(data))
        if 'std' in metrics:
            stats['std'] = float(np.std(data))
        if 'min' in metrics:
            stats['min'] = float(np.min(data))
        if 'max' in metrics:
            stats['max'] = float(np.max(data))
        if 'variance' in metrics:
            stats['variance'] = float(np.var(data))

        stats['count'] = len(measurements)
        stats['accuracy'] = self.calculate_accuracy(measurements)

        return stats

    def visualize_results(self, ammeter_type: str, measurements: List[float]):
        """
        Create visualizations for measurement data

        Args:
            ammeter_type: Type of ammeter
            measurements: List of measurements
        """
        viz_config = self.config['analysis']['visualization']

        if not viz_config.get('enabled', False) or not measurements:
            return

        plot_types = viz_config.get('plot_types', [])
        save_plots = viz_config.get('save_plots', False)
        plot_dir = Path(viz_config.get('plot_dir', 'results/plots'))

        if save_plots:
            plot_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Histogram
        if 'histogram' in plot_types:
            plt.figure(figsize=(10, 6))
            plt.hist(measurements, bins=30, edgecolor='black', alpha=0.7)
            plt.title(f'{ammeter_type.upper()} - Current Distribution')
            plt.xlabel('Current (A)')
            plt.ylabel('Frequency')
            plt.grid(True, alpha=0.3)

            if save_plots:
                plt.savefig(plot_dir / f'{ammeter_type}_histogram_{timestamp}.png')
                self.logger.info(f"Saved histogram for {ammeter_type}")
            else:
                plt.show()
            plt.close()

        # Time Series
        if 'time_series' in plot_types:
            plt.figure(figsize=(12, 6))
            plt.plot(measurements, marker='o', markersize=3, linestyle='-', linewidth=1)
            plt.title(f'{ammeter_type.upper()} - Current Over Time')
            plt.xlabel('Sample Number')
            plt.ylabel('Current (A)')
            plt.grid(True, alpha=0.3)

            if save_plots:
                plt.savefig(plot_dir / f'{ammeter_type}_timeseries_{timestamp}.png')
                self.logger.info(f"Saved time series for {ammeter_type}")
            else:
                plt.show()
            plt.close()

        # Box Plot
        if 'box_plot' in plot_types:
            plt.figure(figsize=(8, 6))
            plt.boxplot(measurements, vert=True)
            plt.title(f'{ammeter_type.upper()} - Current Box Plot')
            plt.ylabel('Current (A)')
            plt.grid(True, alpha=0.3)

            if save_plots:
                plt.savefig(plot_dir / f'{ammeter_type}_boxplot_{timestamp}.png')
                self.logger.info(f"Saved box plot for {ammeter_type}")
            else:
                plt.show()
            plt.close()

    def save_results(self, ammeter_type: str, measurements: List[float], stats: Dict):
        cfg = self.config.get('result_management', {})
        if not cfg.get('save_results'):
            return

        from pathlib import Path

        results_dir = Path(cfg.get('results_dir', 'results/data'))
        results_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{ammeter_type}_{ts}.json"

        data = {
            'ammeter_type': ammeter_type,
            'timestamp': datetime.now().isoformat(),
            'measurements': measurements,
            'statistics': stats
        }

        with open(results_dir / filename, 'w') as f:
            json.dump(data, f, indent=2)

        self.logger.info(f"Saved results to {filename}")

    def run_tests(self):
        """
        Comprehensive test runner for all configured ammeters

        Performs:
        1. Measurement collection
        2. Statistical analysis
        3. Visualization
        4. Result saving

        Returns:
            Dict of test results for all ammeters
        """
        # Dictionary to store results for all ammeters
        comprehensive_results = {}

        # Get list of ammeters from configuration
        ammeter_types = [
            ammeter for ammeter, config
            in self.config['ammeters'].items()
            if config.get('enabled', True)
        ]

        # Run tests for each enabled ammeter
        for ammeter_type in ammeter_types:
            try:
                # Collect measurements
                self.logger.info(f"Starting test for {ammeter_type} ammeter")
                measurements = self.collect_measurements(ammeter_type)

                # Calculate statistics
                stats = self.calculate_statistics(measurements)

                accuracy = stats.get("accuracy")

                threshold = self.config.get("analysis", {}).get("accuracy", {}).get("threshold")

                if threshold is not None and accuracy is not None:
                    if accuracy > threshold:
                        self.logger.warning(
                            f"{ammeter_type} unstable (accuracy={accuracy:.4f}, threshold={threshold})"
                        )

                # Visualize results
                self.visualize_results(ammeter_type, measurements)

                # Save results
                self.save_results(ammeter_type, measurements, stats)

                # Store results
                comprehensive_results[ammeter_type] = {
                    'measurements': measurements,
                    'statistics': stats
                }

                self.logger.info(f"Test completed for {ammeter_type} ammeter")

            except Exception as e:
                self.logger.error(f"Test failed for {ammeter_type} ammeter: {e}")
                comprehensive_results[ammeter_type] = {
                    'error': str(e)
                }

            # Comparative Analysis
        self.comparative_analysis(comprehensive_results)

        # Generate Comprehensive Report
        self.generate_comprehensive_report(comprehensive_results)

    def generate_comprehensive_report(self, results):
        """
        Generate a comprehensive JSON report of test results
        """
        report_config = self.config.get('reporting', {})
        if not report_config.get('generate_report', False):
            self.logger.info("Report generation is disabled")
            return

        try:
            # Create report directory
            report_dir = Path(report_config.get('report_dir', 'results/reports'))
            report_dir.mkdir(parents=True, exist_ok=True)

            # Timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Prepare report data
            report_data = {
                'timestamp': timestamp,
                'total_ammeters_tested': len(results),
                'ammeter_details': {}
            }

            for ammeter_type, data in results.items():
                if 'error' in data:
                    report_data['ammeter_details'][ammeter_type] = {
                        'status': 'FAILED',
                        'error': data['error']
                    }
                else:
                    report_data['ammeter_details'][ammeter_type] = {
                        'status': 'PASSED',
                        'statistics': data.get('statistics', {})
                    }

            # Save report
            json_report_path = report_dir / f'ammeter_test_report_{timestamp}.json'

            with open(json_report_path, 'w') as f:
                json.dump(report_data, f, indent=2)

            self.logger.info(f"Report generated: {json_report_path}")

            return json_report_path

        except Exception as e:
            self.logger.error(f"Failed to generate report: {e}")
            return None

    def comparative_analysis(self, results: Dict):
        self.logger.info("Running comparative analysis...")

        means = {}
        for ammeter, data in results.items():
            if 'statistics' in data and 'mean' in data['statistics']:
                means[ammeter] = data['statistics']['mean']

        if means:
            best = min(means, key=lambda k: means[k])
            self.logger.info(f"Most stable (lowest mean current): {best}")

        return means