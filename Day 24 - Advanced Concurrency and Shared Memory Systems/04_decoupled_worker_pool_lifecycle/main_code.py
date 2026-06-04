"""
Core Topic: Decoupled Process Worker Lifecycles
Description: Demonstrates low-overhead worker isolation structures utilizing plain system queues.
Lead Engineer: Syed Saad Bin Irfan
"""

import multiprocessing
import queue
import time

class IsolatedJobWorker(multiprocessing.Process):
    """Custom process worker that consumes jobs from a shared queue and stops gracefully on a poison pill."""
    def __init__(self, task_queue: multiprocessing.Queue, result_queue: multiprocessing.Queue) -> None:
        super().__init__()
        self.incoming_jobs = task_queue
        self.outgoing_results = result_queue

    def run(self) -> None:
        print(f"[WORKER-{self.pid}] Process loop active and polling.")
        while True:
            try:
                # Block until a job item becomes available in the queue stream
                job_payload = self.incoming_jobs.get(timeout=0.5)
                
                # Check for the shutdown signal (poison pill pattern)
                if job_payload is None:
                    print(f"[WORKER-{self.pid}] Intercepted termination signal. Exiting process loop.")
                    self.incoming_jobs.task_done()
                    break
                    
                # Process the computational payload work task
                computed_output = f"PROCESSED_DATA_NODE_VALUE_{job_payload * 10}"
                self.outgoing_results.put(computed_output)
                self.incoming_jobs.task_done()
                
            except queue.Empty:
                continue

if __name__ == "__main__":
    jobs_stream = multiprocessing.JoinableQueue()
    results_stream = multiprocessing.Queue()

    worker = IsolatedJobWorker(jobs_stream, results_stream)
    worker.start()

    print("[MAIN] Enqueueing workloads down the execution track...")
    for item in [12, 45, 78]:
        jobs_stream.put(item)

    # Inject the poison pill to shut down the worker gracefully once tasks finish
    jobs_stream.put(None)

    jobs_stream.join() # Block until all tasks are fully processed
    
    while not results_stream.empty():
        print(f"[MAIN] Collected computed result: {results_stream.get()}")

    worker.join()