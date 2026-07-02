# Logic Breakdown: Failure Detection Mechanics
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When nodes fail unexpectedly or lose network connectivity, they stop gossiping. The healthy nodes must identify and evict these failed nodes to keep the cluster ring balanced.

## My Approach
I implemented a table evaluation routine. If a node's heartbeat counter falls significantly behind the rest of the cluster during a sync loop, it is flagged as `DEAD`, signaling the cluster routing layers to bypass it.

## Complexity Profile
* Runtime Bounds: Iterates across active listings in linear time $O(N)$.
* Space Constraints: Runs inside constant memory limits $O(1)$.