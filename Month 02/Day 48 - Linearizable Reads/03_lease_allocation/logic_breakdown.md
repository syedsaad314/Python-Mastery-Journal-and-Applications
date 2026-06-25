# Logic Breakdown: Leader Lease Allocation
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Hitting the network for round-trip heartbeats on every single read query slows down performance. We need a way to serve reads locally from memory while guaranteeing that no other leader can exist yet.

## My Approach
I implemented a time-bound lease mechanism. When a leader wins a consensus round, it locks in a short lease window (e.g., 2 seconds). Because followers won't start an election until their heartbeat timeouts expire (which are intentionally set longer than the lease), the leader can safely serve reads from local memory as long as its lease is active.

## Complexity Profile
* Runtime Bounds: Runs instantly in $O(1)$ constant time execution limits.
* Space Constraints: Operates efficiently at $O(1)$ memory weight markers.