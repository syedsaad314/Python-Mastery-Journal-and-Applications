# Logic Breakdown: Unified Cross-Engine Querying
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Data Engineering pipelines often mix legacy Pandas code and modern Polars data pipelines. Joining DataFrames across different framework ecosystems typically requires explicitly converting all data to a single format first.

## My Approach
I utilized DuckDB's automatic Python environment inspection capabilities. When a query references local variables (`df_pandas`, `df_polars`), DuckDB automatically binds to their memory buffers via Arrow/C interfaces, executes the SQL join, and exports the result directly back to Polars (`.pl()`) zero-copy.

## Complexity Profile
* Runtime Bounds: $O(N + M)$ hash join execution time over $N$ Pandas rows and $M$ Polars rows.
* Space Constraints: $O(N + M)$ memory needed to construct the output Polars result DataFrame.