"""
Core Topic: Custom Thread Pools via Queues
Description: Manages a reusable collection of worker threads fed by a synchronized execution queue.
Lead Engineer: Syed Saad Bin Irfan
"""

import queue
import threading
import time
from typing import Callable, Any, Tuple

class CustomThreadPool:
    def __init__(self, fixed_worker_count: int) -> None:
        self.work_queue: queue.Queue = queue.Queue()
        self.workers: list = []
        self._shutdown_sentinel = object()
        
        # Instantiate and anchor dedicated worker threads
        for _ in range(fixed_worker_count):
            t = threading.Thread(target=self._worker_loop)
            t.daemon = True # Allows application to exit cleanly even if thread loops are active
            self.workers.append(t)
            t.start()

    def _worker_loop(self) -> None:
        while True:
            task_item = self.work_queue.get()
            if task_item is self._shutdown_sentinel:
                self.work_queue.task_done()
                break
            
            callable_fn, args = task_item
            try:
                callable_fn(*args)
            except Exception as e:
                print(f"[WORKER ERROR] Handled routine exception: {e}")
            finally:
                self.work_queue.task_done()

    def submit_task(self, task: Callable, *args: Any) -> None:
        self.work_queue.put((task, args))

    def terminate_pool(self) -> None:
        for _ in self.workers:
            self.work_queue.put(self._shutdown_sentinel)
        for t in self.workers:
            t.join()

def process_data_analytics_chunk(chunk_id: int) -> None:
    time.sleep(0.2)
    print(f"[POOL] Processed analytical data fragment batch reference: {chunk_id}")

if __name__ == "__main__":
    pool = CustomThreadPool(fixed_worker_count=3)
    
    for i in range(6):
        pool.submit_task(process_data_analytics_chunk, i)
        
    pool.work_queue.join()  # Blocks until all queued work entries are marked task_done()
    pool.terminate_pool()
    print("[CORE THREAD] Thread pool shutdown completed smoothly.")