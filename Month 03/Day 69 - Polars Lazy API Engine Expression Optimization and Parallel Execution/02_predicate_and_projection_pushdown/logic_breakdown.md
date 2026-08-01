# Logic Breakdown: Predicate & Projection Pushdown
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Reading full Parquet files into memory before applying `.filter()` and `.select()` reads unnecessary byte chunks from disk, blowing up I/O overhead and memory footprints.

## My Approach
I constructed a `pl.scan_parquet()` query tree combining `.filter()` (predicate) and `.select()` (projection). Polars pushes these operations down into the Parquet reader layer. The reader fetches only the `id`, `amount`, and `category` byte columns, skipping `unused_col` entirely and filtering out non-matching row groups before materializing memory buffers.

## Complexity Profile
* Runtime Bounds: $O(M)$ where $M$ is the number of matching records passing pushdown filters.
* Space Constraints: $O(K \times P)$ where $K$ is filtered rows and $P$ is projected columns.