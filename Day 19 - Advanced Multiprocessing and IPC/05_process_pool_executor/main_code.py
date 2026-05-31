"""
Core Topic: High-Level Parallel Execution via ProcessPoolExecutor
Description: Distributes CPU-intensive task arrays across available system cores efficiently.
Lead Engineer: Syed Saad Bin Irfan
"""

from concurrent.futures import ProcessPoolExecutor
import math
import time
from typing import List

def run_cpu_intensive_prime_check(target_integer: int) -> bool:
    """Executes a resource-intensive mathematical verification routine to stress CPU cores."""
    if target_integer <= 1:
        return False
    for factor in range(2, int(math.isqrt(target_integer)) + 1):
        if target_integer % factor == 0:
            return False
    return True

if __name__ == "__main__":
    evaluation_pool = [1000000007, 1000000009, 1000000021, 1000000033, 55555555555]
    
    print(f"[MAIN ENGINE] Initializing ProcessPoolExecutor infrastructure across core grid...")
    start_time = time.perf_counter()
    
    # Enclosing execution in a context manager handles automatic worker teardown and cleanup
    with ProcessPoolExecutor(max_workers=3) as pool_executor:
        # Map automatically splits the task list into chunks and balances the load across processes
        execution_iterator = pool_executor.map(run_cpu_intensive_prime_check, evaluation_pool)
        results: List[bool] = list(execution_iterator)
        
    duration = time.perf_counter() - start_time
    print(f"[MAIN ENGINE] Completed evaluation execution in {duration:.4f} seconds.")
    
    for num, is_prime in zip(evaluation_pool, results):
        print(f" > Integer: {num} | Prime Status Flag: {is_prime}")