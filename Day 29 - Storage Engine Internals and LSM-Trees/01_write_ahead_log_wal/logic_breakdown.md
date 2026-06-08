# Logic Breakdown: Write-Ahead Logging (WAL)
**Engineer:** Syed Saad Bin Irfan

## The Problem
In-memory structures (like MemTables) deliver high performance but are volatile. If a server loses power or encounters a software crash before memory changes are written to disk, recent transactions are permanently lost, violating ACID reliability standards.

## My Approach
I implemented a robust **Write-Ahead Log (WAL)** pipeline that forces changes to be written to a persistent append-only binary file *before* updating volatile memory.

Every transaction is packed with a CRC32 integrity check header using Python's `struct` module. Crucially, the engine calls `os.fsync()` immediately after writing. This forces the operating system to flush kernel page buffers straight to physical disk sectors, providing strong durability guarantees. If a crash occurs, the recovery loop reads the log sequentially to rebuild the correct in-memory state.

## Complexity Profile
* **Runtime Bounds:** Appending operations execute in constant $O(1)$ time. Recovery state playbacks scale linearly at an $O(N)$ rate relative to the size of the log file.
* **Space Constraints:** Requires $O(K)$ memory footprint during recovery to hold the active database keyspace.