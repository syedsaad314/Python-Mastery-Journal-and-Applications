# Logic Breakdown: ReadIndex Tracking
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
If a client reads from a cluster leader immediately after a network partition occurs, the old leader might serve stale data because a new leader has already been elected elsewhere and advanced the state machine log.

## My Approach
I implemented a structural tracking point that captures the leader's current monotonic `commit_index` the millisecond a read call hits the node interface. This value serves as a strict baseline boundary. The node cannot return a response until its local application state has caught up to or passed this index.

## Complexity Profile
* Runtime Bounds: Instant lookup performance operating in constant $O(1)$ boundaries.
* Space Constraints: Fixed item retention footprint scaling at $O(1)$.