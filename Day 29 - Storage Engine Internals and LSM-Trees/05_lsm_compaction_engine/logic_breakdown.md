# Logic Breakdown: LSM-Tree Compaction Engine
**Engineer:** Syed Saad Bin Irfan

## The Problem
As data modifications and tombstone delete records accumulate across separate file layers, multiple versions of the same key waste valuable disk space and slow down system queries over time.

## My Approach
I implemented a structural compaction layer based on a **Log-Structured Merge-Tree (LSM-Tree) Compaction Engine** model.

The engine uses a two-pointer sorting sweep to merge separate file generations into a single consolidated data layer. When encountering duplicate keys across generations, the engine preserves the newer update from the higher-level file and drops the older version automatically. It also filters out expired delete markers (`__TOMBSTONE__`), reclaiming storage space and keeping the system's disk usage lean.

## Complexity Profile
* **Runtime Bounds:** Merging sorted file arrays runs in linear $O(N + M)$ time relative to record counts.
* **Space Constraints:** Scales at $O(N + M)$ memory allocations to process the active record merge buffer.