import json
from pathlib import Path
from datetime import datetime


class AmmeterReporter:
    def __init__(self, logger):
        self.logger = logger

    def save_results(self, ammeter_type, measurements, stats, cfg):
        if not cfg.get('save_results'):
            return

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

    def generate_report(self, results, config):
        report_config = config.get('reporting', {})

        if not report_config.get('generate_report', False):
            self.logger.info("Report generation is disabled")
            return None

        report_dir = Path(report_config.get('report_dir', 'results/reports'))
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        report_data = {
            'timestamp': timestamp,
            'total_ammeters_tested': len(results),
            'ammeter_details': {}
        }

        for name, data in results.items():
            if 'error' in data:
                report_data['ammeter_details'][name] = {
                    'status': 'FAILED',
                    'error': data['error']
                }
            else:
                report_data['ammeter_details'][name] = {
                    'status': 'PASSED',
                    'statistics': data.get('statistics', {})
                }

        path = report_dir / f'ammeter_test_report_{timestamp}.json'

        with open(path, 'w') as f:
            json.dump(report_data, f, indent=2)

        self.logger.info(f"Report generated: {path}")
        return path