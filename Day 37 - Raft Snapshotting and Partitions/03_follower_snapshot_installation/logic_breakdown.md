# Logic Breakdown: Follower Snapshot Installation Enforcement
**Engineer:** Syed Saad Bin Irfan

## The Problem
When a follower receives a complete state snapshot from the leader, it must safely update its local state store and handle any overlapping log history without introducing inconsistencies or corrupting tracking states.

## My Approach
I built a **Follower Snapshot Installation Engine**.

If the incoming snapshot index is completely ahead of the follower's history, the engine discards its entire local log and jumps directly to the snapshot boundary. If the snapshot overlaps with part of its existing log, it retains the remaining valid entries. Finally, it overwrites its key-value store with the new data and updates its internal commit line, safely aligning with the leader.

## Complexity Profile
* **Runtime Bounds:** Clearing logs and applying the snapshot runs in $O(S)$ time, where $S$ is the size of the snapshot data.
* **Space Constraints:** Requires $O(S)$ memory space to ingest and maintain the updated state.