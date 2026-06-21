# Logic Breakdown: Two-Phase Commit Protocol
**Lead Engineer:** Syed Saad Bin Irfan

## The Problem
When data spans multiple physical database instances, committing changes independently can cause partial success states if one node fails mid-way, leaving data inconsistent.

## My Approach
I implemented a baseline **Two-Phase Commit (2PC) Pattern**. 
The process splits writes into a voting/prepare step and a execution/commit step. If every database node votes that its local space is ready (`VOTE_COMMIT`), the central coordinator issues a global command to save the changes. If a single node votes to abort, every node rolls back to maintain data consistency.

## Complexity Profile
* **Runtime Bounds:** Coordination passes execute in $O(N)$ linear time relative to participant count $N$.
* **Space Constraints:** Keeps tracking allocations at a steady $O(1)$ constant overhead.