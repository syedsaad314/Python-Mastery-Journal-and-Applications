# Logic Breakdown: Vectorized Python UDFs in DuckDB
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Row-by-row scalar Python UDFs in database engines incur severe interpreter loop overhead for every record, rendering custom business logic calculations unusable on large datasets.

## My Approach
I registered a vectorized scalar UDF in DuckDB using `type="arrow"`. DuckDB passes underlying Arrow vector chunks directly into the Python function, allowing scalar mathematical calculations to execute in optimized C/NumPy vectorized loops.

## Complexity Profile
* Runtime Bounds: $O(N / B)$ batch invocations where $N$ is total rows and $B$ is vector batch size.
* Space Constraints: $O(B)$ memory allocation for vector inputs and output vectors.