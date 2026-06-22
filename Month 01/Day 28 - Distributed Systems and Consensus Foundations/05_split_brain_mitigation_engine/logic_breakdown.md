# Logic Breakdown: Network Partition Split-Brain Mitigation
**Engineer:** Syed Saad Bin Irfan

## The Problem
When a network failure splits a cluster into isolated groups, nodes on both sides may assume the other group failed. If a minority cluster segment continues electing leaders and accepting writes independently, it creates a severe **Split-Brain** scenario that corrupts configuration records.

## My Approach
I built a defensive partition wrangler that runs a strict **Self-Demotion Quorum Evaluation Routine**.

The core leader logic forces continuous connectivity validation checks against the cluster membership pool during heartbeat sweeps. If the number of acknowledging peer nodes drops below the strict majority quorum threshold ($\lfloor N/2 \rfloor + 1$), the leader steps down to a `FOLLOWER` state immediately, neutralizing the minority partition and preventing dirty data mutations.

## Complexity Profile
* **Runtime Bounds:** Network connectivity checks and collection intersection evaluations execute in linear $O(P)$ time relative to active peer counts.
* **Space Constraints:** Keeps memory consumption flat at a constant $O(N)$ structural footprint.