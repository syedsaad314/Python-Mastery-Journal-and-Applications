# Logic Breakdown: Raft Leader Election and Term State Machine
**Engineer:** Syed Saad Bin Irfan

## The Problem
In a distributed network, nodes must dynamically elect a single coordinate leader without relying on a central authority. If multiple nodes attempt to become leaders simultaneously, it can cause split votes, preventing the cluster from reaching consensus.

## My Approach
I implemented a robust **Raft Leader Election State Machine** utilizing randomized timeouts.

Nodes start as `FOLLOWER` nodes. If they do not receive a heartbeat within a randomized window (between 150ms and 300ms), they transition to `CANDIDATE`, increment their local term counter, and request votes from peers. Adding random variance (jitter) to the timeouts ensures that one node will timeout first and secure a majority vote before competitors can cause a split-vote scenario.

## Complexity Profile
* **Runtime Bounds:** Timeout evaluations and state transitions execute in $O(1)$ constant time. Solicitations scale linearly at $O(N)$ with the cluster size.
* **Space Constraints:** Requires $O(N)$ memory allocations to store cluster peer identities.