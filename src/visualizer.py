from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

PLOTTERS = {
    "histogram": lambda plt, data: plt.hist(data, bins=30),
    "time_series": lambda plt, data: plt.plot(data),
    "box_plot": lambda plt, data: plt.boxplot(data),
}


class AmmeterVisualizer:
    def __init__(self, logger):
        self.logger = logger

    def visualize_results(self, ammeter_type: str, measurements, viz_config):
        if not viz_config.enabled or not measurements:
            return

        plot_types = viz_config.plot_types
        save_plots = viz_config.save_plots
        plot_dir = Path(viz_config.plot_dir)

        if save_plots:
            plot_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for plot_type in plot_types:
            if plot_type not in PLOTTERS:
                continue

            plt.figure(figsize=(10, 6))

            PLOTTERS[plot_type](plt, measurements)

            plt.title(f'{ammeter_type.upper()} - {plot_type.replace("_", " ").title()}')

            if save_plots:
                filename = f"{ammeter_type}_{plot_type}_{timestamp}.png"
                plt.savefig(plot_dir / filename)
                self.logger.info(f"Saved {plot_type} for {ammeter_type}")
            else:
                plt.show()

            plt.close()