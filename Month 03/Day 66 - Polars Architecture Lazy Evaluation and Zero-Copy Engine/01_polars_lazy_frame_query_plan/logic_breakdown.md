# Logic Breakdown: Polars LazyFrame & Query Plan Optimization
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Eager DataFrame operations (like standard Pandas) execute every filter and select immediately in memory. This reads unneeded columns (missing projection pushdown) and evaluates unfiltered rows (missing predicate pushdown), exhausting memory bandwidth.

## My Approach
I constructed a Polars `LazyFrame` processing graph. Instead of calculating immediately, Polars builds a Logical Plan. During execution optimization, Polars pushes `filter` operations down to the data reader source and drops unneeded columns (`payload_bytes`) prior to allocation.

## Complexity Profile
* Runtime Bounds: $O(K)$ where $K$ is the filtered subset size (rather than $O(N)$ full dataset size).
* Space Constraints: Reduces peak memory allocation by pruning unselected columns before evaluation.