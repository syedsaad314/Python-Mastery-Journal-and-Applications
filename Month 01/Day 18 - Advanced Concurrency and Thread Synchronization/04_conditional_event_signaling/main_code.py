"""
Core Topic: Inter-Thread Conditional Event Signaling
Description: Uses thread events to coordinate complex execution phases across disparate workers.
Lead Engineer: Syed Saad Bin Irfan
"""

import threading
import time

class SystemInitializationOrchestrator:
    def __init__(self) -> None:
        self.system_ready_event = threading.Event()

    def process_background_boot_sequence(self) -> None:
        print("[BOOT WORKER] Initializing micro-kernels and reading disk configurations...")
        time.sleep(1.5)
        print("[BOOT WORKER] Internal subsystems ready. Setting global event high signal flag.")
        self.system_ready_event.set()

    def await_system_activation(self, microservice_name: str) -> None:
        print(f"[{microservice_name}] Up and awaiting global engine ready signal status...")
        self.system_ready_event.wait()  # Blocks efficiently until set() is explicitly invoked
        print(f"[{microservice_name}] Active signal acquired. Launching operations pipeline.")

if __name__ == "__main__":
    orchestrator = SystemInitializationOrchestrator()
    
    service_a = threading.Thread(target=orchestrator.await_system_activation, args=("User Authentication Service",))
    service_b = threading.Thread(target=orchestrator.await_system_activation, args=("Payment Processing Engine",))
    boot_worker = threading.Thread(target=orchestrator.process_background_boot_sequence)

    service_a.start()
    service_b.start()
    time.sleep(0.1)
    boot_worker.start()

    service_a.join()
    service_b.join()
    boot_worker.join()