# Logic Breakdown: Log Compaction and Snapshotting
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
An append-only log grows larger over time, consuming valuable disk space and causing long delays when a restarting node replays the log history from scratch.

## My Approach
I implemented a **Snapshot Log Compactor Engine**.
Instead of retaining a long history of every value change, the compactor squashes old entries into a single key-value snapshot state dictionary. Once the state snapshot is written to disk, the redundant historical logs are safely purged, saving storage space and speeding up node restart recovery times.

## Complexity Profile
* **Runtime Bounds:** Compacting logs scales linearly at $O(H)$ relative to total historical entry length $H$.
* **Space Constraints:** Reduces memory from an unbounded log to a bounded state footprint of $O(K)$ keys.