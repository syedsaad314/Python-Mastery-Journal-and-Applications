# Logic Breakdown: Memory Footprint Evaluation
**Engineer:** Syed Saad Bin Irfan

## The Problem
Using the wrong data structures can quietly inflate memory usage, causing servers running data-heavy workloads to run out of RAM unnecessarily.

## My Approach
I built a clean benchmarking harness around `sys.getsizeof()` to evaluate the exact memory usage of Python's primary collections holding identical datasets.

The output reveals the internal memory footprint of different data structures. Lists are compact and memory-efficient, whereas Sets and Dicts sacrifice memory space for fast, hash-based lookups ($O(1)$). Understanding these memory trade-offs helps developers choose the best data structure based on hardware constraints.

## Complexity Profile
* **Runtime Bounds:** Constant time $O(1)$ calculations per container check.
* **Space Constraints:** Zero additional memory overhead during execution.