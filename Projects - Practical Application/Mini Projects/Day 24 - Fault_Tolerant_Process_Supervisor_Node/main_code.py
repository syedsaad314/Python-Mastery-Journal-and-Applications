"""
System: Fault-Tolerant Distributed Process Supervisor Node
Description: A resilient process orchestration layer that monitors active worker processes, 
             automatically replaces crashed workers, and intercepts unexpected failures cleanly.
Lead Engineer: Syed Saad Bin Irfan
"""

import multiprocessing
import logging
import time
import os
import random
import sys

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (Supervisor-Engine) %(message)s')

def brittle_worker_runtime_simulation(worker_identity_string: str) -> None:
    """A sample worker process loop designed to crash randomly to test supervisor recovery mechanisms."""
    logging.info(f"Worker process [{worker_identity_string}] initialized on system PID: {os.getpid()}")
    time.sleep(0.4)
    
    # Introduce an unstable environment trigger that throws an unhandled exception 50% of the time
    if random.choice([True, False]):
        logging.error(f"Worker [{worker_identity_string}] encountered a fatal runtime exception.")
        raise RuntimeError("Fatal process memory corruption simulation.")
        
    logging.info(f"Worker [{worker_identity_string}] completed its tasks successfully.")
    sys.exit(0)


class ClusterProcessSupervisor:
    """Monitors background process lifecycles and automatically runs recovery boots for dropped nodes."""
    def __init__(self, configured_worker_nodes: list) -> None:
        self.node_registry_list = configured_worker_nodes
        # Map worker names to active process instances
        self.active_process_map: dict[str, multiprocessing.Process] = {}

    def spawn_worker_node(self, worker_name: str) -> None:
        """Spins up a new child process worker instance and tracks it in the management map."""
        proc = multiprocessing.Process(
            target=brittle_worker_runtime_simulation, 
            args=(worker_name,), 
            name=worker_name
        )
        self.active_process_map[worker_name] = proc
        proc.start()
        logging.info(f"Supervisor successfully booted node '{worker_name}' on system PID: {proc.pid}")

    def initialize_cluster(self) -> None:
        """Spins up all registered cluster worker nodes."""
        logging.info("Initializing clustering setup controls...")
        for node_name in self.node_registry_list:
            self.spawn_worker_node(node_name)

    def monitor_and_heal_cluster_loop(self, maximum_reboots: int = 3) -> None:
        """Monitors active processes and automatically triggers reboots if any workers drop offline."""
        reboot_counters_map = {name: 0 for name in self.node_registry_list}
        
        while True:
            active_nodes_count = len(self.active_process_map)
            if active_nodes_count == 0:
                logging.info("All registered cluster jobs processed. Exiting monitoring loops.")
                break
                
            for node_name, process_instance in list(self.active_process_map.items()):
                # Check if the process has terminated
                if not process_instance.is_alive():
                    exit_code = process_instance.exitcode
                    logging.warning(f"Detected offline cluster node: '{node_name}' (Exit Code: {exit_code})")
                    
                    if exit_code != 0: # Node crashed or exited with an error status code
                        if reboot_counters_map[node_name] < maximum_reboots:
                            logging.info(f"Attempting self-healing reboot cycle for failed node '{node_name}'...")
                            reboot_counters_map[node_name] += 1
                            self.spawn_worker_node(node_name)
                        else:
                            logging.error(f"Node '{node_name}' breached maximum failure limits ({maximum_reboots}). Permanent exclusion applied.")
                            del self.active_process_map[node_name]
                    else:
                        logging.info(f"Node '{node_name}' exited cleanly with zero issues. Removing from registry tracks.")
                        del self.active_process_map[node_name]
                        
            time.sleep(0.2) # Prevent high CPU usage by throttling the polling loop


if __name__ == "__main__":
    print("\n=== SYSTEM START: DISTRIBUTED PROCESS SUPERVISOR NODE ===\n")
    
    target_nodes = ["DATA_INGEST_NODE_01", "COMPUTE_NODE_02", "AGGREGATOR_NODE_03"]
    
    supervisor = ClusterProcessSupervisor(target_nodes)
    supervisor.initialize_cluster()
    
    # Start the tracking and recovery loop
    supervisor.monitor_and_heal_cluster_loop(maximum_reboots=2)
    
    print("\n=== SYSTEM SHUTDOWN: CLUSTER MANAGEMENT CYCLE OUTCOME METRICS STABLE ===")