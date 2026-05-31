"""
System: Resilient Background Task Worker Matrix
Description: A fault-tolerant task manager that schedules intensive compute workloads across persistent,
             monitored worker processes and automatically restarts failed nodes to maintain operations.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
import multiprocessing
import queue
import random
import time
from typing import Dict, List, Tuple, Any, Optional

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (%(threadName)s) %(message)s')

class MatrixTask:
    def __init__(self, task_id: str, payload_value: int) -> None:
        self.task_id: str = task_id
        self.payload_value: int = payload_value

class ResilientWorkerNode:
    def __init__(self, node_id: str, task_inbound_queue: multiprocessing.Queue, results_outbound_queue: multiprocessing.Queue) -> None:
        self.node_id: str = node_id
        self.in_q: multiprocessing.Queue = task_inbound_queue
        self.out_q: multiprocessing.Queue = results_outbound_queue
        self.process_handle: Optional[multiprocessing.Process] = None

    def _worker_runtime_loop(self) -> None:
        """Executes tasks continuously, including intentional logic failures for testing resilience."""
        while True:
            task_item: Optional[MatrixTask] = self.in_q.get()
            if task_item is None:  # Shutdown sentinel matched
                break
                
            # Simulate a system failure to verify recovery mechanisms
            if task_item.payload_value == -999:
                logging.error(f"[NODE-{self.node_id}] Critical failure triggered. Terminating process...")
                os._exit(1) # type: ignore # Force-exit the process to simulate a sudden crash
                
            # Simulate heavy computational processing time
            time.sleep(0.1)
            calculated_factorial_root = sum(range(task_item.payload_value))
            
            response_payload = {
                "task_id": task_item.task_id,
                "node_assigned": self.node_id,
                "calculated_output": calculated_factorial_root,
                "timestamp_completed": time.time()
            }
            self.out_q.put(response_payload)

    def launch_node(self) -> None:
        """Spawns the worker runtime inside a separate process."""
        self.process_handle = multiprocessing.Process(
            target=self._worker_runtime_loop,
            name=f"MatrixNode-{self.node_id}"
        )
        self.process_handle.start()


class WorkerMatrixCoordinator:
    def __init__(self, target_node_capacity: int = 3) -> None:
        self.node_capacity: int = target_node_capacity
        self.jobs_ipc_queue: multiprocessing.Queue = multiprocessing.Queue()
        self.results_ipc_queue: multiprocessing.Queue = multiprocessing.Queue()
        self.nodes_registry: Dict[str, ResilientWorkerNode] = {}

    def submit_workload(self, task_id: str, math_input: int) -> None:
        self.jobs_ipc_queue.put(MatrixTask(task_id, math_input))

    def _monitor_and_reap_nodes(self) -> None:
        """Monitors active processes and automatically spawns replacement nodes if a crash occurs."""
        for node_id, worker_node in self.nodes_registry.items():
            handle = worker_node.process_handle
            if handle and not handle.is_alive():
                logging.warning(f"Coordinator: Detected failure on node '{node_id}'. Spawning replacement...")
                
                # Provision and launch a clean replacement node instance
                replacement_node = ResilientWorkerNode(node_id, self.jobs_ipc_queue, self.results_ipc_queue)
                replacement_node.launch_node()
                self.nodes_registry[node_id] = replacement_node

    def execute_matrix_lifecycle(self, targeted_jobs_count: int) -> List[Dict[str, Any]]:
        """Coordinates task lifecycle management, node health monitoring, and results processing."""
        # Provision initial cluster allocation
        for i in range(self.node_capacity):
            node_id = f"COMPUTE-LN-{i}"
            node = ResilientWorkerNode(node_id, self.jobs_ipc_queue, self.results_ipc_queue)
            node.launch_node()
            self.nodes_registry[node_id] = node

        compiled_matrix_results: List[Dict[str, Any]] = []

        # Monitor loop continues until expected results are collected
        while len(compiled_matrix_results) < targeted_jobs_count:
            # Regularly check process health statuses
            self._monitor_and_reap_nodes()
            
            try:
                # Non-blocking result capture to keep monitor checks active
                successful_payload = self.results_ipc_queue.get(timeout=0.1)
                compiled_matrix_results.append(successful_payload)
            except queue.Empty:
                continue

        # Clean up and shut down active processes safely
        logging.info("Workload processing complete. Stopping active background workers...")
        for _ in range(self.node_capacity):
            self.jobs_ipc_queue.put(None)

        for worker_node in self.nodes_registry.values():
            if worker_node.process_handle:
                worker_node.process_handle.join()

        return compiled_matrix_results

if __name__ == "__main__":
    print("\n=== SYSTEM START: RESILIENT BACKGROUND TASK MATRIX COORDINATOR ===\n")
    coordinator = WorkerMatrixCoordinator(target_node_capacity=3)

    # Enqueue standard compute tasks
    coordinator.submit_workload("TASK_01", 50000)
    coordinator.submit_workload("TASK_02", 75000)
    
    # Inject an explicit failure task to test recovery capabilities
    coordinator.submit_workload("TASK_CRASH_TRIGGER", -999)
    
    coordinator.submit_workload("TASK_03", 120000)
    coordinator.submit_workload("TASK_04", 35000)

    # Run execution coordination loop tracking standard non-failed metrics tasks
    matrix_output_records = coordinator.execute_matrix_lifecycle(targeted_jobs_count=4)

    print(f"\n=== QUANTUM WORKER MATRIX CALCULATED RUNTIME DATA ===\n")
    print(json.dumps(matrix_output_records, indent=4)) # type: ignore