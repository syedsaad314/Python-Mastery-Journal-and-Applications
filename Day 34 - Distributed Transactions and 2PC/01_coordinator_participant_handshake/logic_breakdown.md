# Logic Breakdown: Coordinator-Participant Handshake Model
**Engineer:** Syed Saad Bin Irfan

## The Problem
In multi-node environments, a coordinator cannot unilaterally tell nodes to write data because an individual node might have lock conflicts, constraint violations, or local storage failures that force an abort.

## My Approach
I modeled Phase 1 of the **Two-Phase Commit Protocol (2PC)**, known as the **Prepare or Voting Phase**.

The coordinator broadcasts a prepare message to all participating nodes. Each node runs local checks, validates its isolation guarantees, and returns a vote. The global system can only commit if the vote matrix contains unanimous approvals. If a single node experiences a conflict and registers an abort vote, the entire distributed state machine shifts toward a rollback state.

## Complexity Profile
* **Runtime Bounds:** Gathering votes scales linearly at $O(N)$ with respect to the total number of participating shards $N$.
* **Space Constraints:** Storing the returned votes uses $O(N)$ memory tracking space.