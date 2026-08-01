# Logic Breakdown: Parallel Multi-Threaded GroupBy
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Single-threaded aggregation algorithms build a single central hash map, creating memory locking contention and leaving multi-core CPU architectures underutilized.

## My Approach
I executed Polars' `group_by().agg()` pipeline. Polars uses lock-free multithreaded Rayon execution under the hood, partitioning the input data into concurrent hash tables per thread worker before running parallel merge steps on intermediate key-value maps.

## Complexity Profile
* Runtime Bounds: $O(N / T)$ runtime where $N$ is row count and $T$ is available CPU hardware thread worker count.
* Space Constraints: $O(U)$ space where $U$ is the number of unique partition keys.