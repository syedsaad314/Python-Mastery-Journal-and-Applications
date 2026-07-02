# Logic Breakdown: State Infection Mechanics
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When information is received via gossip, the engine must distinguish between fresh updates and outdated messages to prevent old data from overriding newer cluster states.

## My Approach
I built a data mutation merge engine that checks entry keys. The local table is updated only if the incoming heartbeat counter strictly exceeds the currently stored local counter value.

## Complexity Profile
* Runtime Bounds: Runs in linear time $O(M)$ matching the length of the incoming map.
* Space Constraints: Mutates the dictionary in-place, keeping auxiliary overhead at $O(1)$.