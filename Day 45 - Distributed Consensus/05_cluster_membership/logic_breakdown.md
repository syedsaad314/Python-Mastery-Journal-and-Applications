# Logic Breakdown: Dynamic Cluster Membership Tracking
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When scaling out a cluster, adding or removing nodes on the fly can cause configuration mismatches, where different nodes calculate different quorum majorities simultaneously.

## My Approach
I engineered a **Dynamic Cluster Membership Tracker**.
The tracker maintains the list of active cluster members inside a set. When the group membership changes, the tracker updates the active member pool and recalculates the strict majority quorum threshold. This ensures all nodes remain aligned on configuration metrics and prevents split-quorum mistakes during cluster scaling.

## Complexity Profile
* **Runtime Bounds:** Configuration membership adjustments execute in $O(1)$ constant time.
* **Space Constraints:** Memory usage scales linearly at $O(M)$ based on total active cluster members $M$.