# Portfolio Architectural Review: Replicated Key-Value Store System
**Lead Engineer:** Syed Saad Bin Irfan

## Practical Context
In cloud infrastructure and microservice platforms, foundational tools like distributed key-value stores need to stay highly available and perfectly coordinated. If a database node crashes or suffers a hardware fault, the remaining cluster instances must seamlessly choose a new coordinator and keep processing data accurately, preventing downtime or data conflicts.

## Core Problem Space & Challenges
1. **Split-Brain Election Hazards:** If a network failure splits a cluster in two, both sides might try to elect a leader independently, creating conflicting split-brain states.
2. **Out-of-Date Log Rewrites:** If a node with an outdated or incomplete log is elected leader, it could accidentally overwrite valid, committed history on other nodes, leading to data loss.
3. **Consensus Write Alignment:** The system must guarantee that a write command is only applied to individual node state machines once it is successfully stored by a clear majority quorum across the cluster.

## My Technical Solution & Implementation Approach
* **Strict Majority Quorum Enforcement:** The cluster uses a strict majority quorum rule to validate elections and write operations. A candidate can only become leader, and a command can only be committed, if approved by a majority of nodes ($\lfloor N/2 \rfloor + 1$). This protects the cluster from split-brain scenarios during network partitions.
* **Up-to-Date Leader Constraints:** Followers review a candidate's log history before voting. A follower will deny its vote if the candidate's last log entry has an older term, or if terms match but the candidate's log is shorter than the follower's. This ensures the elected leader contains all previously committed cluster logs.
* **Decoupled Architecture Composition:** The implementation is split across 6 clean, dedicated modules (`state.py`, `storage.py`, `node.py`, `cluster.py`, `metrics.py`, and `main.py`). This clean decoupling separates consensus state, storage engines, and network communication layers, ensuring code clarity and easy maintainability.

## Complexity Profile Analysis
* **Runtime Bounds:**
  * RequestVote and AppendEntries Validations: Processing state and term checks runs in fast $O(1)$ constant time per RPC request.
  * Cluster Broadcast Replications: Broadcasting entries across the cluster network scales linearly at $O(N)$ relative to total node count $N$.
* **Memory Constraints:** System memory use grows linearly at $O(L + N)$ to store the log entries history $L$ and manage active node configurations $N$.