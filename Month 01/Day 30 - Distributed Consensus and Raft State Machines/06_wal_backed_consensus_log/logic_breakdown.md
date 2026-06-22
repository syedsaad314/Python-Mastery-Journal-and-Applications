# Logic Breakdown: WAL-Backed Consensus Log Systems
**Engineer:** Syed Saad Bin Irfan

## The Problem
If a consensus node reboots, losing its log history breaks the State Machine Replication model. When the node rejoins the cluster, its missing history could break consistency guarantees or overwrite valid data during term synchronization updates.

## My Approach
I built a binary **Consensus Log Persistence** layer to ensure data survives system reboots.

Every consensus entry is packed with its current term index and string payload length into a clean binary block using the `struct` pattern. Calling `os.fsync()` forces the OS to save updates directly to disk before returning success. On startup, the node reads this binary log file sequentially, restoring its complete consensus history up to the point of interruption.

## Complexity Profile
* **Runtime Bounds:** Appending records runs in constant $O(1)$ time, while recovery reads scale linearly ($O(L)$) with the length of the log file.
* **Space Constraints:** Rebuilding history requires $O(L)$ memory allocations to load the restored record array.