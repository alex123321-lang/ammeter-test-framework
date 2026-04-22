from datetime import datetime


class TestSession:
    def __init__(self, config):
        self.timestamp = datetime.now()
        self.config = config
        self.results = {}  # ammeter_type -> TestResult

    def add_result(self, result):
        self.results[result.ammeter_type] = result

    def get_successful(self):
        return {
            k: v for k, v in self.results.items()
            if v.is_success
        }

    def get_failed(self):
        return {
            k: v for k, v in self.results.items()
            if not v.is_success
        }

    def summary(self):
        total = len(self.results)
        success = len(self.get_successful())
        failed = len(self.get_failed())

        return {
            "total": total,
            "success": success,
            "failed": failed
        }