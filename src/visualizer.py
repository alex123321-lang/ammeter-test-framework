from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt


class AmmeterVisualizer:
    def __init__(self, logger):
        self.logger = logger

    def visualize_results(self, ammeter_type: str, measurements, viz_config: dict):
        if not viz_config.get('enabled', False) or not measurements:
            return

        plot_types = viz_config.get('plot_types', [])
        save_plots = viz_config.get('save_plots', False)
        plot_dir = Path(viz_config.get('plot_dir', 'results/plots'))

        if save_plots:
            plot_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if 'histogram' in plot_types:
            plt.figure(figsize=(10, 6))
            plt.hist(measurements, bins=30)
            plt.title(f'{ammeter_type.upper()} - Current Distribution')

            if save_plots:
                plt.savefig(plot_dir / f'{ammeter_type}_histogram_{timestamp}.png')
                self.logger.info(f"Saved histogram for {ammeter_type}")
            else:
                plt.show()

            plt.close()

        if 'time_series' in plot_types:
            plt.figure(figsize=(12, 6))
            plt.plot(measurements)
            plt.title(f'{ammeter_type.upper()} - Current Over Time')

            if save_plots:
                plt.savefig(plot_dir / f'{ammeter_type}_timeseries_{timestamp}.png')
                self.logger.info(f"Saved time series for {ammeter_type}")
            else:
                plt.show()

            plt.close()

        if 'box_plot' in plot_types:
            plt.figure(figsize=(8, 6))
            plt.boxplot(measurements)
            plt.title(f'{ammeter_type.upper()} - Current Box Plot')

            if save_plots:
                plt.savefig(plot_dir / f'{ammeter_type}_boxplot_{timestamp}.png')
                self.logger.info(f"Saved box plot for {ammeter_type}")
            else:
                plt.show()

            plt.close()