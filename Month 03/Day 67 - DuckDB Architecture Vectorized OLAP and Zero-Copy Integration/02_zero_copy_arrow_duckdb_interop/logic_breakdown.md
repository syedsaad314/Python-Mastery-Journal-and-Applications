# Logic Breakdown: Zero-Copy Apache Arrow Querying
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Passing large datasets between in-memory tabular structures (Arrow $\rightarrow$ SQL Engine) usually forces serialization/ingestion passes, consuming double the RAM and incurring memory-copy latency.

## My Approach
I leveraged `duckdb.arrow()` to register PyArrow Tables directly into DuckDB's execution framework. DuckDB scans Apache Arrow C-Data interface memory pointers in-place, eliminating memory copying while maintaining full SQL query capabilities.

## Complexity Profile
* Runtime Bounds: $O(K)$ where $K$ is the number of matching records in the filter.
* Space Constraints: $O(1)$ extra heap allocation; reuses existing Arrow buffer pointers.