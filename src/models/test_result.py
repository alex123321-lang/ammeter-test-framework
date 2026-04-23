class TestResult:
    def __init__(self, ammeter_type, measurements, statistics, error=None, error_type=None, meta=None):
        self.ammeter_type = ammeter_type
        self.measurements = measurements
        self.statistics = statistics
        self.error = error
        self.error_type = error_type
        self.meta = meta or {}

    @property
    def is_success(self):
        return self.error is None