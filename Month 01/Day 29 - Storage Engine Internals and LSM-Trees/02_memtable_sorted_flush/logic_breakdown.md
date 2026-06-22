# Logic Breakdown: In-Memory MemTable Sorted Buffering
**Engineer:** Syed Saad Bin Irfan

## The Problem
Writing values directly to separate data files on disk causes random I/O delays, which quickly limits application throughput. We need an memory buffer to absorb incoming writes quickly while keeping keys sorted for fast retrieval.

## My Approach
I built a data buffering container called a **MemTable**. 

Instead of writing straight to disk, values are buffered in memory while tracking data sizes closely. When total bytes hit the configured capacity threshold limit, the system triggers an automated **SSTable Flush Pass**. It extracts entries, sorts them by key, and writes them sequentially into an immutable disk file, converting expensive random writes into highly efficient sequential operations.

## Complexity Profile
* **Runtime Bounds:** Memory insertions run in average-case $O(1)$ time, while sorting entries for a flush takes $O(N \log N)$ steps.
* **Space Constraints:** Strictly bounded to the explicit byte-size capacity threshold limit configured at initialization.