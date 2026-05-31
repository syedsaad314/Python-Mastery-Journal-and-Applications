"""
Core Topic: Process Synchronization via BaseManager
Description: Shares live custom state machine instances across process boundaries using network proxy loops.
Lead Engineer: Syed Saad Bin Irfan
"""

from multiprocessing.managers import BaseManager
import queue
import time

class MetricsStateTracker:
    def __init__(self) -> None:
        self.telemetry_logs = []

    def log_event(self, description: str) -> None:
        self.telemetry_logs.append(description)

    def retrieve_logs(self) -> list:
        return self.telemetry_logs

class RemoteClusterManager(BaseManager): 
    """Custom manager class to register and expose our state tracker object."""
    pass

if __name__ == "__main__":
    # Register the custom state container class with the manager exposure hooks
    RemoteClusterManager.register("StateTracker", MetricsStateTracker)
    
    # Launch an internal manager server instance bound to local runtime parameters
    with RemoteClusterManager() as centralized_manager:
        # Instantiate the exposed proxy object instance
        shared_state_proxy = centralized_manager.StateTracker() # type: ignore
        
        print("[SERVER MANAGER] Component established. Modifying from primary orchestration scope...")
        shared_state_proxy.log_event("SYSTEM_BOOT_SUCCESS")
        
        # Verify that access loops route correctly through proxy representations
        print(f"[SERVER MANAGER] Current shared state contents: {shared_state_proxy.retrieve_logs()}")