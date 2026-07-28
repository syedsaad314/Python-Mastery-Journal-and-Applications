# Logic Breakdown: Memory-Bounded Chunk Processing
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Loading multi-gigabyte CSV or Parquet files directly into memory with `pd.read_csv` causes Out-Of-Memory (OOM) crashes on resource-constrained compute nodes.

## My Approach
I leveraged Pandas' `chunksize` iterator parameter. By processing fixed-size batches (e.g., 100 to 10,000 rows at a time), state is accumulated globally (`total_sum`, `total_count`) and memory used by individual chunks is discarded by Python's garbage collector after each loop iteration.

## Complexity Profile
* Runtime Bounds: $O(N)$ linear pass over input stream rows.
* Space Constraints: Strict $O(K)$ bounded memory footprint, where $K$ is the chunk size.