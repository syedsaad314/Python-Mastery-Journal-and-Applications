# Logic Breakdown: 3PC Phase 2 - Pre-Commit Isolation Phase
**Engineer:** Syed Saad Bin Irfan

## The Problem
Without a dedicated preparation step, nodes cannot distinguish between a transaction that failed early and one that was approved by all peers but cut off by a coordinator crash.

## My Approach
I built a **Pre-Commit Isolation Phase Orchestrator**.

Once Phase 1 passes successfully, the coordinator moves the system into Phase 2 (`Pre-Commit`). In this phase, participants acquire their local resource locks and enter a state of readiness. This step guarantees that all nodes have reviewed the request and are prepared to commit, making it safe for nodes to complete the transaction on their own if the coordinator goes offline.

## Complexity Profile
* **Runtime Bounds:** Processes acknowledgments in linear $O(N)$ time for $N$ nodes.
* **Space Constraints:** Map tracking structures require $O(N)$ space.