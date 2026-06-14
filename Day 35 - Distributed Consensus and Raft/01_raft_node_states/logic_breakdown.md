# Logic Breakdown: Raft Node State Machine
**Engineer:** Syed Saad Bin Irfan

## The Problem
A Raft node must change its role dynamically depending on cluster conditions (e.g., leader failure or heartbeat timeouts). Uncontrolled or random state changes can cause multiple nodes to act as leader simultaneously, corrupting data logs.

## My Approach
I implemented a structured **Raft Role State Engine** that acts as a guard rail for state transitions.

Nodes start in the `FOLLOWER` state. If they stop receiving heartbeats, they transition to `CANDIDATE` to request votes. If they secure a cluster majority, they transition to `LEADER`. If at any point they discover a node with a higher term count, they immediately step down and revert back to `FOLLOWER`. This state machine forms the baseline for consensus safety.

## Complexity Profile
* **Runtime Bounds:** State evaluations and adjustments execute in $O(1)$ constant time.
* **Space Constraints:** Requires $O(1)$ constant memory allocation space.