import socket
import time

class MeasurementTimeoutError(Exception):
    pass

class MeasurementConnectionError(Exception):
    pass

class MeasurementEmptyDataError(Exception):
    pass


class AmmeterCollector:
    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def request_measurement(port: int, command: bytes, timeout: int = 2) -> float:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect(('localhost', port))
                s.sendall(command)
                data = s.recv(1024)

                if not data:
                    raise MeasurementEmptyDataError(f"No data received from port {port}")

                return float(data.decode("utf-8"))

        except socket.timeout:
            raise MeasurementTimeoutError(f"Timeout connecting to port {port}")

        except Exception as e:
            raise MeasurementConnectionError(str(e))

    def collect_measurements(self, ammeter_type, cfg, sampling_config):
        return list(self.stream_measurements(ammeter_type, cfg, sampling_config))

    def stream_measurements(self, ammeter_type, cfg, sampling_config):
        port = cfg.port
        command = cfg.command.encode("utf-8")

        num = sampling_config.measurements_count
        freq = sampling_config.sampling_frequency_hz
        timeout = sampling_config.timeout_seconds

        interval = 1.0 / freq if freq > 0 else 0.1

        self.logger.info(
            f"Collecting {num} measurements from {ammeter_type} at {freq}Hz"
        )

        for i in range(num):
            start = time.time()

            measurement = self.request_measurement(port, command, timeout)

            self.logger.debug(
                f"[{i + 1}/{num}] {ammeter_type}: {measurement:.4f}A"
            )

            yield measurement

            elapsed = time.time() - start
            time.sleep(max(0, interval - elapsed))

        self.logger.info(f"Finished streaming {ammeter_type}")