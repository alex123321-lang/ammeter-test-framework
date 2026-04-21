import numpy as np

METRICS = {
    "mean": np.mean,
    "median": np.median,
    "std": np.std,
    "min": np.min,
    "max": np.max,
    "variance": np.var,
}

class AmmeterAnalyzer:
    def __init__(self, logger):
        self.logger = logger

    def calculate_accuracy(self, measurements):
        if not measurements:
            return float('inf')

        data = np.array(measurements, dtype=float)

        mean = float(np.mean(data))
        std = float(np.std(data))

        return std / mean if mean != 0 else float('inf')

    def calculate_statistics(self, measurements, metrics):
        if not measurements:
            return {}

        data = np.array(measurements)

        stats = {}

        for metric in metrics:
            if metric in METRICS:
                stats[metric] = float(METRICS[metric](data))

        stats['count'] = len(measurements)
        stats['accuracy'] = self.calculate_accuracy(measurements)

        return stats