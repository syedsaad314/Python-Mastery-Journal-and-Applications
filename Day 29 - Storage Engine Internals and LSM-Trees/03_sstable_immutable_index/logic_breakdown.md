# Logic Breakdown: Sparse Indexing and Immutable SSTable Querying
**Engineer:** Syed Saad Bin Irfan

## The Problem
As immutable data tables (SSTables) multiply on disk, searching every file sequentially for a key creates heavy disk I/O load. Conversely, loading every key's file offset directly into memory uses too much RAM, causing memory pressure as the dataset scales.

## My Approach
I implemented a space-efficient **Sparse In-Memory Index Array** search pipeline.

Instead of indexing every single row, the engine samples keys at fixed block intervals (e.g., every 2nd or 100th record) and logs their byte offsets in memory. When a query is executed, the engine runs a fast memory lookup over the sparse index map to locate the exact file block boundary. It then seeks directly to that byte offset and reads a small data window sequentially, optimizing performance while using minimal memory.

## Complexity Profile
* **Runtime Bounds:** Locating block boundaries in memory takes $O(\log K)$ time (where $K$ is sparse index depth), followed by a small bounded file read pass.
* **Space Constraints:** Compresses memory indexing usage down to a fraction ($1/\text{Interval}$) of the total keyspace.