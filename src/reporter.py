import json
from pathlib import Path
from datetime import datetime


class AmmeterReporter:
    def __init__(self, logger):
        self.logger = logger

    def save_results(self, ammeter_type, measurements, stats, cfg):
        if not cfg.save_results:
            return

        results_dir = Path(cfg.results_dir)
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

    def generate_report(self, results, config):
        report_config = config.reporting

        if not report_config.generate_report:
            self.logger.info("Report generation is disabled")
            return None

        report_dir = Path(report_config.report_dir)
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        report_data = {
            'timestamp': timestamp,
            'total_ammeters_tested': len(results),
            'ammeter_details': {}
        }

        for ammeter_type, result in results.items():

            if not result.is_success:
                report_data['ammeter_details'][ammeter_type] = {
                    'status': 'FAILED',
                    'error': result.error
                }
            else:
                report_data['ammeter_details'][ammeter_type] = {
                    'status': 'PASSED',
                    'statistics': result.statistics
                }

        path = report_dir / f'ammeter_test_report_{timestamp}.json'

        with open(path, 'w') as f:
            json.dump(report_data, f, indent=2)

        self.logger.info(f"Report generated: {path}")
        return path