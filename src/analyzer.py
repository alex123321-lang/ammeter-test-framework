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
        self.reset()

    def reset(self):
        self.count = 0
        self.sum = 0.0
        self.values = []  # keep if you still want full stats

    def update(self, value: float):
        self.count += 1
        self.sum += value
        self.values.append(value)

    def finalize(self, metrics):
        if self.count == 0:
            return {}

        data = np.array(self.values)

        stats = {}

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

        stats['count'] = self.count
        stats['accuracy'] = self._accuracy(data)

        return stats

    def _accuracy(self, data):
        mean = float(np.mean(data))
        std = float(np.std(data))
        return std / mean if mean != 0 else float("inf")