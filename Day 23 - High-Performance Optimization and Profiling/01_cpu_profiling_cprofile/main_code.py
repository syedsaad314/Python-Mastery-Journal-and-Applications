"""
Core Topic: Programmatic CPU Profiling
Description: Uses native cProfile and pstats to locate execution hotspots and sorting metrics.
Lead Engineer: Syed Saad Bin Irfan
"""

import cProfile
import pstats
import time
from typing import List

def heavy_computation_loop() -> List[int]:
    """Simulates a dense processing workload containing an unintended execution bottleneck."""
    results = []
    for i in range(10000):
        # Simulating a micro-delay hotspot via repetitive checks
        if i % 2 == 0:
            results.append(i)
    return results

def inefficient_lookup_hotspot() -> None:
    """Simulates a common execution bottleneck using flat arrays instead of sets."""
    data_pool = list(range(5000))
    # Repeatedly lookup entries causing quadratic scale bottlenecks
    for target in range(1000):
        _ = target in data_pool

if __name__ == "__main__":
    print("[PROFILER] Starting targeted performance collection pass...")
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Execute workloads inside the profiler bounds
    heavy_computation_loop()
    inefficient_lookup_hotspot()
    
    profiler.disable()
    print("[PROFILER] Workloads completed. Generating metrics visualization matrix:\n")
    
    # Process results sorting strictly by total internal execution duration
    stats_viewer = pstats.Stats(profiler)
    stats_viewer.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats(10)