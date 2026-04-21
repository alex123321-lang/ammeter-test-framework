import threading
import time
from Ammeters.Circutor_Ammeter import CircutorAmmeter
from Ammeters.Entes_Ammeter import EntesAmmeter
from Ammeters.Greenlee_Ammeter import GreenleeAmmeter
from Ammeters.client import request_current_from_ammeter


def run_greenlee_emulator():
    GreenleeAmmeter(5001).start_server()


def run_entes_emulator():
    EntesAmmeter(5002).start_server()


def run_circutor_emulator():
    CircutorAmmeter(5003).start_server()


if __name__ == "__main__":
    # Start each ammeter in a separate thread
    threading.Thread(target=run_greenlee_emulator, daemon=True).start()
    threading.Thread(target=run_entes_emulator, daemon=True).start()
    threading.Thread(target=run_circutor_emulator, daemon=True).start()

    # Wait for servers to start
    time.sleep(2)

    # Fixed commands - now matching what ammeters expect:
    request_current_from_ammeter(5001, b'MEASURE_GREENLEE -get_measurement')
    request_current_from_ammeter(5002, b'MEASURE_ENTES -get_data')
    request_current_from_ammeter(5003, b'MEASURE_CIRCUTOR -get_measurement')

    while True:
        time.sleep(1)
