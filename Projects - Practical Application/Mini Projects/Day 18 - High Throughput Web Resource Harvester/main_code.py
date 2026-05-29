"""
System: High-Throughput Web Resource Harvester
Description: A thread-safe data extraction harvester that orchestrates parallel worker tasks,
             implements granular per-domain rate limiting, and protects against worker thread starvation.
Lead Engineer: Syed Saad Bin Irfan
"""

import logging
import json
import queue
import random
import threading
import time
from typing import Any, Dict, List, Tuple

# Setup structured logging diagnostics
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(threadName)s] %(message)s')

class DomainRateLimiter:
    def __init__(self) -> None:
        self._last_access_times: Dict[str, float] = {}
        self._registry_lock: threading.Lock = threading.Lock()

    def enforce_rate_delay(self, target_domain: str, required_interval_sec: float) -> None:
        """Enforces a strict thread-safe minimum time interval between consecutive requests to a domain."""
        with self._registry_lock:
            current_time = time.time()
            last_accessed = self._last_access_times.get(target_domain, 0.0)
            elapsed_time = current_time - last_accessed

            if elapsed_time < required_interval_sec:
                enforced_wait = required_interval_sec - elapsed_time
                logging.info(f"Rate Limiter: Throttling traffic for domain '{target_domain}'. Waiting {enforced_wait:.2f}s...")
                time.sleep(enforced_wait)
            
            # Update access records post-execution window closure
            self._last_access_times[target_domain] = time.time()


class HighThroughputHarvester:
    def __init__(self, total_workers: int = 3) -> None:
        self.task_inbound_queue: queue.Queue = queue.Queue()
        self.aggregated_results: List[Dict[str, Any]] = []
        self.results_lock: threading.Lock = threading.Lock()
        self.rate_limiter = DomainRateLimiter()
        self.workers_pool: List[threading.Thread] = []
        self._shutdown_sentinel = object()
        self.worker_count = total_workers

    def enqueue_harvest_task(self, target_url: str, server_domain: str, rules_delay: float) -> None:
        """Submits target coordinates into the data collection pipeline."""
        self.task_inbound_queue.put((target_url, server_domain, rules_delay))
        logging.info(f"Enqueued target harvest route: {target_url}")

    def _worker_harvest_loop(self) -> None:
        while True:
            payload_item = self.task_inbound_queue.get()
            
            # Check for the shutdown signal to exit the loop cleanly
            if payload_item is self._shutdown_sentinel:
                self.task_inbound_queue.task_done()
                break

            target_url, server_domain, rules_delay = payload_item
            try:
                # Apply rate-limiting policies before initiating requests
                self.rate_limiter.enforce_rate_delay(server_domain, rules_delay)
                
                # Simulate a network scraping payload step
                logging.info(f"Processing remote extraction point: {target_url}")
                time.sleep(random.uniform(0.1, 0.3)) # Simulate realistic request-response overhead
                
                extracted_mock_payload = {
                    "source_url": target_url,
                    "bytes_retrieved": random.randint(2048, 8192),
                    "execution_status": 200
                }

                # Securely append findings to the shared results collection
                with self.results_lock:
                    self.aggregated_results.append(extracted_mock_payload)

            except Exception as failure:
                logging.error(f"Execution fault encountered inside ingestion step: {str(failure)}")
            finally:
                # Mark the task as completed to keep queue tracking accurate
                self.task_inbound_queue.task_done()

    def boot_harvester_cluster(self) -> None:
        logging.info(f"Starting {self.worker_count} background data harvester threads...")
        for i in range(self.worker_count):
            t = threading.Thread(target=self._worker_harvest_loop, name=f"HarvesterWorker-{i}")
            t.daemon = True
            self.workers_pool.append(t)
            t.start()

    def shutdown_harvester_cluster(self) -> None:
        logging.info("Sending termination signals to worker threads...")
        for _ in range(self.worker_count):
            self.task_inbound_queue.put(self._shutdown_sentinel)
        for t in self.workers_pool:
            t.join()
        logging.info("All background harvester instances safely terminated.")


if __name__ == "__main__":
    print("\n=== INITIALIZING WEB RESOURCE HARVESTER PROTOCOL ===\n")
    harvester = HighThroughputHarvester(total_workers=3)

    # Populate tasks, introducing repeated domains to trigger rate limiter defenses
    harvester.enqueue_harvest_task("https://uok.edu.pk/departments/cs/metrics", "uok.edu.pk", 1.0)
    harvester.enqueue_harvest_task("https://uok.edu.pk/departments/cs/faculty", "uok.edu.pk", 1.0)
    harvester.enqueue_harvest_task("https://github.com/syedsaad314/logs", "github.com", 0.5)
    harvester.enqueue_harvest_task("https://github.com/syedsaad314/repo", "github.com", 0.5)
    harvester.enqueue_harvest_task("https://linkedin.com/in/saad", "linkedin.com", 1.5)

    harvester.boot_harvester_cluster()

    # Block main thread execution context until all tasks are cleared
    harvester.task_inbound_queue.join()
    harvester.shutdown_harvester_cluster()

    print("\n=== EXTRACTION MATRIX RUN SUMMARY ===")
    print(f"Total Successful Records Saved: {len(harvester.aggregated_results)}")
    print(f"Raw Ingestion Array Sample Data Payload:")
    print(json.dumps(harvester.aggregated_results[:2], indent=2))