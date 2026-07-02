# Logic Breakdown: Heartbeat Sequence Tracking
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Nodes need a simple way to declare to the rest of the cluster that they are healthy and processing events, without relying on physical server clocks.

## My Approach
I implemented a logical increment counter on each node. Every time a node starts a new gossip cycle, it advances its own heartbeat counter by one, signaling to the cluster that it is actively running.

## Complexity Profile
* Runtime Bounds: $O(1)$ constant increment operations.
* Space Constraints: Space requirements are constant at $O(1)$.