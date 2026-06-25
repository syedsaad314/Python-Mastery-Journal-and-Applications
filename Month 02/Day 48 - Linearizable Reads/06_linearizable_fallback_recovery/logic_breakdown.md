# Logic Breakdown: Linearizable Fallback Mechanics
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Lease windows are fragile. During high system load, background garbage collection pauses, or sudden scheduling delays, a leader's lease can expire mid-flight. The engine needs a graceful fallback to prevent dropping or misprocessing read queries.

## My Approach
I built a defensive branching controller that evaluates the lease expiration timestamp against the system clock for every read request. If the lease has expired or is close to expiring, the engine dynamically triggers a fallback route that executes a full ReadIndex quorum confirmation check across the network.

## Complexity Profile
* Runtime Bounds: Evaluates instantly in constant time bounds of $O(1)$.
* Space Constraints: Uses a zero-allocation footprint profile of $O(1)$.