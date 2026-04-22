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

    def generate_report(self, session):
        config = session.config.reporting

        if not config.generate_report:
            self.logger.info("Report generation is disabled")
            return

        report_dir = Path(config.report_dir)
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = session.timestamp.strftime("%Y%m%d_%H%M%S")

        report_data = {
            "timestamp": timestamp,
            "summary": session.summary(),
            "ammeters": {}
        }

        for ammeter, result in session.results.items():
            if not result.is_success:
                report_data["ammeters"][ammeter] = {
                    "status": "FAILED",
                    "error": result.error
                }
            else:
                report_data["ammeters"][ammeter] = {
                    "status": "PASSED",
                    "statistics": result.statistics
                }

        path = report_dir / f"ammeter_test_report_{timestamp}.json"

        with open(path, "w") as f:
            import json
            json.dump(report_data, f, indent=2)

        self.logger.info(f"Report generated: {path}")