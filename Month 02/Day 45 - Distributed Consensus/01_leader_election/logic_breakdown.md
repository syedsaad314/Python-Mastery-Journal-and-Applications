# Logic Breakdown: Raft Leader Election State Transitions
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
Distributed clusters must always have exactly one valid leader processing writes. If a leader crashes, the cluster needs to detect the failure and safely choose a new leader without causing split-brain conflicts.

## My Approach
I implemented a **Raft Leader Election State Machine**.
Nodes start as `Follower` instances. If they don't receive a heartbeat before their randomized election timeout expires, they transition to the `Candidate` role. The candidate increments its election term counter, votes for itself, and requests votes from its peers. If it wins a strict majority quorum of votes, it is promoted to `Leader`, preventing split-brain conditions.

## Complexity Profile
* **Runtime Bounds:** Quorum state verification runs in $O(1)$ constant time.
* **Space Constraints:** Requires a fixed $O(1)$ constant runtime memory layout.