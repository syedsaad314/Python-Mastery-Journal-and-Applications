# Logic Breakdown: Advanced OLAP SQL Window Functions
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Analytical queries requiring partitioned running totals, intra-group rankings, or previous row offsets (`LAG`) are slow and complex when constructed using self-joins in traditional SQL engines.

## My Approach
I executed DuckDB's native window function engine (`OVER (PARTITION BY ... ORDER BY ...)`). DuckDB partitions records in vector memory, sorts by frame keys, and computes window calculations inline in a single parallelized execution pass.

## Complexity Profile
* Runtime Bounds: $O(N \log N)$ due to intra-partition sorting.
* Space Constraints: $O(N)$ vector tracking structures for window frame boundary indexing.