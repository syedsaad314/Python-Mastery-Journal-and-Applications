# Logic Breakdown: Out-Of-Core Parquet Scanning
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Analyzing multi-gigabyte Parquet datasets on memory-constrained infrastructure causes OOM (Out Of Memory) exceptions if the query engine attempts to load entire files into system RAM.

## My Approach
I utilized DuckDB's `read_parquet()` file streaming engine configured with `SET max_memory='16MB'`. DuckDB reads Parquet metadata, selectively loads requested columnar byte chunks, streams data vectors through operators, and automatically spills intermediate partition buffers to disk if memory limits are reached.

## Complexity Profile
* Runtime Bounds: $O(N)$ linear file scan pass.
* Space Constraints: Strict $O(M)$ memory cap, where $M$ is configured `max_memory`.