class AmmeterComparator:
    def __init__(self, logger):
        self.logger = logger

    def comparative_analysis(self, session):
        self.logger.info("Running comparative analysis...")

        self.logger.info("Running comparative analysis...")

        means = {}

        for ammeter, result in session.results.items():
            if result.statistics and "mean" in result.statistics:
                means[ammeter] = result.statistics["mean"]

        if means:
            best = min(means, key=lambda k: means[k])
            self.logger.info(f"Most stable (lowest mean current): {best}")

        return means