import socket
import time


class AmmeterCollector:
    def __init__(self, logger):
        self.logger = logger

    def request_measurement(self, port: int, command: bytes, timeout: int = 2) -> float:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect(('localhost', port))
                s.sendall(command)
                data = s.recv(1024)

                if data:
                    return float(data.decode('utf-8'))
                else:
                    self.logger.warning(f"No data received from port {port}")
                    return None

        except socket.timeout:
            self.logger.error(f"Timeout connecting to port {port}")
            return None

        except Exception as e:
            self.logger.error(f"Error requesting measurement from port {port}: {e}")
            return None

    def collect_measurements(self, ammeter_type: str, ammeter_config, sampling_config) -> list:
        port = ammeter_config.port
        command = ammeter_config.command.encode('utf-8')

        num_measurements = sampling_config.measurements_count
        frequency = sampling_config.sampling_frequency_hz
        timeout = sampling_config.timeout_seconds

        measurements = []
        interval = 1.0 / frequency if frequency > 0 else 0.1

        self.logger.info(
            f"Collecting {num_measurements} measurements from {ammeter_type} at {frequency}Hz"
        )

        for i in range(num_measurements):
            start_time = time.time()

            m = self.request_measurement(port, command, timeout)
            if m is not None:
                measurements.append(m)

            elapsed = time.time() - start_time
            time.sleep(max(0, interval - elapsed))

        self.logger.info(f"Collected {len(measurements)} measurements from {ammeter_type}")
        return measurements