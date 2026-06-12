# Logic Breakdown: Write-Ahead Log (WAL) Recovery Architecture
**Engineer:** Syed Saad Bin Irfan

## The Problem
If a server crashes or loses power unexpectedly, any transactions stored only in volatile memory are lost, leading to data loss or database corruption.

## My Approach
I implemented a **Write-Ahead Logging (WAL) System model**.

The node must append an operation to a persistent, append-only log file on disk before updating its volatile memory space. If the server crashes, the internal state can be completely recovered. On reboot, the system reads and replays the log file sequentially, reconstructing the volatile memory state up to the exact point of the failure.

## Complexity Profile
* **Runtime Bounds:** Appending log entries runs in $O(1)$ constant time. Reconstructing state scales linearly at $O(E)$ based on the total number of logged entries $E$.
* **Space Constraints:** Storage metrics scale at $O(E)$ to preserve the historical audit trail.