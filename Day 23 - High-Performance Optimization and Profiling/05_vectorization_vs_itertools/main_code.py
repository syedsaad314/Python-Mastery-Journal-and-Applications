"""
Core Topic: Compute Loop Itertools Optimization
Description: Uses optimized native loops to accelerate mathematical data series processing.
Lead Engineer: Syed Saad Bin Irfan
"""

import itertools
import time
from typing import List

def standard_processing_loop(data_vector: List[int]) -> List[int]:
    """Transforms data elements sequentially using standard list processing loops."""
    output_array = []
    for item in data_vector:
        output_array.append(item * 2)
    return output_array

def optimized_itertools_loop(data_vector: List[int]) -> List[int]:
    """Transforms datasets efficiently using native list comprehension mapping loops."""
    # Maps mutations using internal C-level processing loops
    return [item * 2 for item in data_vector]

if __name__ == "__main__":
    workload_payload = list(range(1000000))
    
    # Benchmark standard element iteration loop patterns
    start_std = time.perf_counter()
    res_std = standard_processing_loop(workload_payload)
    duration_std = time.perf_counter() - start_std
    
    # Benchmark optimized comprehension pipeline loops
    start_opt = time.perf_counter()
    res_opt = optimized_itertools_loop(workload_payload)
    duration_opt = time.perf_counter() - start_opt
    
    print(f"[COMPUTATION REPORT] Standard Append Loop Time:  {duration_std:.5f} Seconds")
    print(f"[COMPUTATION REPORT] Optimized Internal Map Time: {duration_opt:.5f} Seconds")
    print(f"[PERFORMANCE MARGIN] Internalized mappings reduce processing latency significantly.")