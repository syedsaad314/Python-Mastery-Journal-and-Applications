# Logic Breakdown: Coordinator Transaction State Tracking
**Engineer:** Syed Saad Bin Irfan

## The Problem
In multi-shard transactions, if a central coordinator loses track of its state mid-flight, it can issue conflicting commands to different shards, leading to data corruption and broken consistency guarantees.

## My Approach
I implemented a strict **Finite State Machine (FSM)** for the transaction coordinator.

The FSM restricts state changes to valid paths, ensuring a transaction starts at `INIT`, moves to `PREPARING` to collect shard votes, and then transitions to either a definitive `COMMITTED` or `ABORTED` state. This structure makes the transaction's lifecycle predictable and easy to audit.

## Complexity Profile
* **Runtime Bounds:** Updating and validating state transitions runs in $O(1)$ constant time.
* **Space Constraints:** Storage overhead is $O(P)$ relative to the number of participants $P$ tracking their votes.