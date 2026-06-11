# Logic Breakdown: Sloppy Quorum and Hinted Handoff Execution
**Engineer:** Syed Saad Bin Irfan

## The Problem
Under a strict quorum model ($R + W > N$), if too many primary replicas crash or go offline, write operations are blocked entirely, hurting the system's write availability.

## My Approach
I implemented a **Sloppy Quorum Strategy with Hinted Handoff**.

If the primary servers assigned to a data key are unreachable, the cluster routes the write request to an available backup node outside the key's immediate replication group. The backup node saves the data along with a metadata "hint" indicating where the write belongs. Once the primary server recovers, the backup node detects it is back online and replays the stored updates, restoring data consistency without blocking incoming writes.

## Complexity Profile
* **Runtime Bounds:** Saving a hinted write takes $O(1)$ constant time. Replaying hints scales linearly at $O(H)$ based on the number of updates stored in the handoff queue.
* **Space Constraints:** Memory usage scales linearly at $O(H)$ to hold queued updates on the backup node.