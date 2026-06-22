"""
Core Topic: Multi-Producer Multi-Consumer IPC Queues
Description: Coordinates data routing across multiple worker processes using thread-safe, process-safe queues.
Lead Engineer: Syed Saad Bin Irfan
"""

import multiprocessing
import queue
import time
from typing import List

def analytics_consumer_worker(task_queue: multiprocessing.Queue, output_list: multiprocessing.Queue) -> None:
    """Processes elements from the queue until it encounters a shutdown sentinel."""
    while True:
        try:
            # Non-blocking fetch to allow clean timeout loops
            data_item = task_queue.get(timeout=1.0)
            if data_item is None:  # Termination sentinel signature matched
                break
            
            # Process and transform the data chunk
            result_string = f"PROCESSED_VAL::{data_item * 10}"
            output_list.put(result_string)
        except queue.Empty:
            continue

if __name__ == "__main__":
    jobs_queue: multiprocessing.Queue = multiprocessing.Queue()
    results_queue: multiprocessing.Queue = multiprocessing.Queue()
    workers_pool: List[multiprocessing.Process] = []
    
    # Provision 3 active consumer worker nodes
    for i in range(3):
        p = multiprocessing.Process(
            target=analytics_consumer_worker, 
            args=(jobs_queue, results_queue),
            name=f"ConsumerNode-{i}"
        )
        workers_pool.append(p)
        p.start()

    # Enqueue raw metric data fragments
    raw_metrics = [12, 45, 78, 90, 122]
    print(f"[MAIN PROCESS] Dispatching {len(raw_metrics)} items into shared IPC task queue...")
    for item in raw_metrics:
        jobs_queue.put(item)

    # Append shutdown sentinels to match total active worker nodes
    for _ in range(3):
        jobs_queue.put(None)

    for p in workers_pool:
        p.join()

    # Empty out results gathered into the destination pipeline queue
    compiled_data = []
    while not results_queue.empty():
        compiled_data.append(results_queue.get())
        
    print(f"[MAIN PROCESS] Collected aggregated process data results:\n{compiled_data}")