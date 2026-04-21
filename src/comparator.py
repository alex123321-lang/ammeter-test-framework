class AmmeterComparator:
    def __init__(self, logger):
        self.logger = logger

    def comparative_analysis(self, results):
        self.logger.info("Running comparative analysis...")

        means = {}

        for ammeter, data in results.items():
            if 'statistics' in data and 'mean' in data['statistics']:
                means[ammeter] = data['statistics']['mean']

        if means:
            best = min(means, key=lambda k: means[k])
            self.logger.info(f"Most stable (lowest mean current): {best}")

        return means