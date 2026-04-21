import numpy as np


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